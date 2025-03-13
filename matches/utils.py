from django.db import transaction
from datetime import timedelta
import random

from manager_game.models import Rivalry
from matches.models import Match
from wrestler.models import Wrestler, WrestlerBrand

def generate_matches_for_day(game, day_number):
    """Helper function to generate matches for a specific day."""
    brands = list(game.brands.all())
    ppv_events = list(game.ppv_events.filter(season=game.season).order_by('date'))  # Филтрираме по текущия сезон
    num_brands = len(brands)
    cycle_length = num_brands + 1
    num_ppv = len(ppv_events)

    position = (day_number - 1) % cycle_length
    match_types = ['singles', 'triple_threat', 'fatal_four_way', 'ladder_match', 'hell_in_a_cell']
    participant_requirements = {
        'singles': 2,
        'triple_threat': 3,
        'fatal_four_way': 4,
        'ladder_match': 2,
        'hell_in_a_cell': 2,
        'royal_rumble': 30,
    }

    used_wrestlers = set()

    if position < num_brands:
        # Brand day
        current_brand = brands[position]
        wrestler_brands = WrestlerBrand.objects.filter(brand=current_brand)
        all_wrestlers = Wrestler.objects.filter(brand_links__in=wrestler_brands).distinct()

        male_wrestlers = list(all_wrestlers.filter(gender='male'))
        female_wrestlers = list(all_wrestlers.filter(gender='female'))

        num_matches = random.randint(3, 5)
        for _ in range(num_matches):
            wrestlers_pool = random.choice(
                [male_wrestlers, female_wrestlers]) if male_wrestlers and female_wrestlers else (
                    male_wrestlers or female_wrestlers)
            if not wrestlers_pool:
                continue

            available_wrestlers = [w for w in wrestlers_pool if w not in used_wrestlers]
            max_participants = len(available_wrestlers)
            valid_match_types = [
                mt for mt in match_types if participant_requirements[mt] <= max_participants
            ]
            if not valid_match_types:
                continue

            match_type = random.choice(valid_match_types)
            required_participants = participant_requirements[match_type]

            participants = random.sample(available_wrestlers, required_participants)
            match = Match.objects.create(
                user=game.user,
                game=game,
                match_type=match_type,
                day_number=day_number,
                season=game.season,  # Задаваме текущия сезон
                brand=current_brand,
                championship=None
            )
            match.participants.set(participants)
            used_wrestlers.update(participants)
    else:
        # PPV day
        ppv_index = ((day_number - 1) // cycle_length) % num_ppv
        current_ppv = ppv_events[ppv_index]
        generate_ppv_matches(game, current_ppv, day_number)

def generate_ppv_matches(game, ppv_event, day_number):
    """
    Generate matches for a PPV event, ensuring all championships have a match.
    """
    match_types = ['singles', 'triple_threat', 'fatal_four_way', 'ladder_match', 'hell_in_a_cell']
    brands = list(game.brands.all())
    championships = list(game.championships.all())
    wrestlers = list(game.wrestlers.all())
    rivalries = Rivalry.objects.filter(game=game, completed=False)

    min_matches = len(championships)
    total_matches = max(min_matches, random.randint(5, 10))

    created_matches = []
    used_wrestlers = set()

    # Step 1: Championship matches
    for championship in championships:
        available_wrestlers = [
            w for w in wrestlers
            if w not in used_wrestlers and w.gender == championship.gender
        ]
        if not available_wrestlers:
            continue

        participants = []
        current_champion = championship.current_champion

        if current_champion and current_champion not in used_wrestlers:
            participants.append(current_champion)
            challengers = [w for w in available_wrestlers if w != current_champion]
            if challengers:
                participants.append(random.choice(challengers))
        else:
            if len(available_wrestlers) >= 2:
                participants = random.sample(available_wrestlers, 2)

        if len(participants) == 2:
            match = Match.objects.create(
                user=game.user,
                game=game,
                match_type='singles',
                day_number=day_number,
                season=game.season,  # Задаваме текущия сезон
                ppv_event=ppv_event,
                brand=random.choice(brands) if brands else None,
                championship=championship
            )
            match.participants.set(participants)
            created_matches.append(match)
            used_wrestlers.update(participants)

    # Step 2: Rivalry matches
    remaining_matches = total_matches - len(created_matches)
    if remaining_matches > 0:
        for rivalry in rivalries:
            if len(created_matches) >= total_matches:
                break
            wrestler_one = rivalry.wrestler_one
            wrestler_two = rivalry.wrestler_two
            if wrestler_one in used_wrestlers or wrestler_two in used_wrestlers:
                continue

            match = Match.objects.create(
                user=game.user,
                game=game,
                match_type='singles',
                day_number=day_number,
                season=game.season,  # Задаваме текущия сезон
                ppv_event=ppv_event,
                brand=rivalry.brand,
                championship=None
            )
            match.participants.set([wrestler_one, wrestler_two])
            created_matches.append(match)
            used_wrestlers.add(wrestler_one)
            used_wrestlers.add(wrestler_two)

    # Step 3: Brand-based matches
    remaining_matches = total_matches - len(created_matches)
    if remaining_matches > 0 and brands:
        for brand in brands:
            if remaining_matches <= 0:
                break
            wrestler_brands = WrestlerBrand.objects.filter(brand=brand)
            brand_wrestlers = Wrestler.objects.filter(brand_links__in=wrestler_brands)
            available_wrestlers = [w for w in brand_wrestlers if w not in used_wrestlers]
            if len(available_wrestlers) >= 2:
                num_participants = random.choice([2, 3, 4])
                participants = random.sample(available_wrestlers, min(num_participants, len(available_wrestlers)))
                match = Match.objects.create(
                    user=game.user,
                    game=game,
                    match_type=random.choice(match_types),
                    day_number=day_number,
                    season=game.season,  # Задаваме текущия сезон
                    ppv_event=ppv_event,
                    brand=brand,
                    championship=None
                )
                match.participants.set(participants)
                created_matches.append(match)
                used_wrestlers.update(participants)
                remaining_matches -= 1

    # Step 4: Random matches
    remaining_matches = total_matches - len(created_matches)
    if remaining_matches > 0:
        available_wrestlers = [w for w in wrestlers if w not in used_wrestlers]
        while remaining_matches > 0 and len(available_wrestlers) >= 2:
            num_participants = random.choice([2, 3, 4])
            participants = random.sample(available_wrestlers, min(num_participants, len(available_wrestlers)))
            match = Match.objects.create(
                user=game.user,
                game=game,
                match_type=random.choice(match_types),
                day_number=day_number,
                season=game.season,  # Задаваме текущия сезон
                ppv_event=ppv_event,
                brand=random.choice(brands) if brands else None,
                championship=None
            )
            match.participants.set(participants)
            created_matches.append(match)
            used_wrestlers.update(participants)
            remaining_matches -= 1
            available_wrestlers = [w for w in wrestlers if w not in used_wrestlers]

    return created_matches