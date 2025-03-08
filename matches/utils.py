from django.db import transaction
from datetime import timedelta
import random

from manager_game.models import Rivalry
from matches.models import Match
from wrestler.models import Wrestler, WrestlerBrand


def generate_matches_for_day(game, day_number):
    """Helper function to generate matches for a specific day."""
    brands = list(game.brands.all())
    ppv_events = list(game.ppv_events.all().order_by('date'))
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

    # Множество за проследяване на използваните кечисти за деня
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

            # Филтрираме само кечисти, които още не са използвани
            available_wrestlers = [w for w in wrestlers_pool if w not in used_wrestlers]
            max_participants = len(available_wrestlers)
            valid_match_types = [
                mt for mt in match_types if participant_requirements[mt] <= max_participants
            ]
            if not valid_match_types:  # Няма достатъчно свободни кечисти
                continue

            match_type = random.choice(valid_match_types)
            required_participants = participant_requirements[match_type]

            participants = random.sample(available_wrestlers, required_participants)
            match = Match.objects.create(
                user=game.user,
                game=game,
                match_type=match_type,
                day_number=day_number,
                brand=current_brand,
                championship=None  # Обикновените дни нямат мачове за титли
            )
            match.participants.set(participants)
            # Добавяме участниците към използваните
            used_wrestlers.update(participants)
    else:
        # PPV day
        ppv_index = ((day_number - 1) // cycle_length) % num_ppv
        current_ppv = ppv_events[ppv_index]
        generate_ppv_matches(game, current_ppv, day_number)  # Извикваме generate_ppv_matches за PPV дни


def generate_ppv_matches(game, ppv_event, day_number):
    """
    Generate matches for a PPV event, ensuring all championships have a match.
    - If a championship has a current champion, they must participate.
    - If a championship is vacant, two wrestlers compete for it.
    - Each wrestler can participate only once per day.
    - Number of matches: random between 5 and 10, adjusted to include all championships.
    """
    match_types = ['singles', 'triple_threat', 'fatal_four_way', 'ladder_match', 'hell_in_a_cell']
    brands = list(game.brands.all())
    championships = list(game.championships.all())
    wrestlers = list(game.wrestlers.all())
    rivalries = Rivalry.objects.filter(game=game, completed=False)

    # Ensure at least enough matches to cover all championships
    min_matches = len(championships)
    total_matches = max(min_matches, random.randint(5, 10))

    # Track used wrestlers and created matches
    created_matches = []
    used_wrestlers = set()

    # Step 1: Generate championship matches (mandatory for each championship)
    for championship in championships:
        available_wrestlers = [
            w for w in wrestlers
            if w not in used_wrestlers and w.gender == championship.gender
        ]
        if not available_wrestlers:
            continue  # Skip if no eligible wrestlers remain

        participants = []
        current_champion = championship.current_champion

        if current_champion and current_champion not in used_wrestlers:
            # Champion defends the title
            participants.append(current_champion)
            remaining_spots = 1  # Singles match by default for simplicity
            challengers = [w for w in available_wrestlers if w != current_champion]
            if challengers:
                participants.append(random.choice(challengers))
        else:
            # Vacant title: select two random wrestlers
            if len(available_wrestlers) >= 2:
                participants = random.sample(available_wrestlers, 2)

        if len(participants) == 2:  # Ensure we have enough participants
            match = Match.objects.create(
                user=game.user,
                game=game,
                match_type='singles',  # Default to singles for championship matches
                day_number=day_number,
                ppv_event=ppv_event,
                brand=random.choice(brands) if brands else None,
                championship=championship  # Добавяме титлата към мача
            )
            match.participants.set(participants)
            created_matches.append(match)
            used_wrestlers.update(participants)

    # Step 2: Generate matches based on active rivalries
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
                ppv_event=ppv_event,
                brand=rivalry.brand,
                championship=None  # Ривалските мачове не са за титли
            )
            match.participants.set([wrestler_one, wrestler_two])
            created_matches.append(match)
            used_wrestlers.add(wrestler_one)
            used_wrestlers.add(wrestler_two)

    # Step 3: Generate brand-based matches
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
                    ppv_event=ppv_event,
                    brand=brand,
                    championship=None  # Бранд мачовете не са за титли
                )
                match.participants.set(participants)
                created_matches.append(match)
                used_wrestlers.update(participants)
                remaining_matches -= 1

    # Step 4: Fill remaining matches with random wrestlers
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
                ppv_event=ppv_event,
                brand=random.choice(brands) if brands else None,
                championship=None  # Случайните мачове не са за титли
            )
            match.participants.set(participants)
            created_matches.append(match)
            used_wrestlers.update(participants)
            remaining_matches -= 1
            available_wrestlers = [w for w in wrestlers if w not in used_wrestlers]

    return created_matches