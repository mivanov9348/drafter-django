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
    # 'royal_rumble' excluded from random selection due to its unique size requirement

    participant_requirements = {
        'singles': 2,
        'triple_threat': 3,
        'fatal_four_way': 4,
        'ladder_match': 2,  # Can have more, but 2 is minimum
        'hell_in_a_cell': 2,
        'royal_rumble': 30,
    }

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

            # Filter match types based on available wrestlers
            max_participants = len(wrestlers_pool)
            valid_match_types = [
                mt for mt in match_types if participant_requirements[mt] <= max_participants
            ]
            if not valid_match_types:  # Need at least 2 wrestlers for any match
                continue

            match_type = random.choice(valid_match_types)
            required_participants = participant_requirements[match_type]

            participants = random.sample(wrestlers_pool, required_participants)
            match = Match.objects.create(
                user=game.user,
                game=game,
                match_type=match_type,
                day_number=day_number,
                brand=current_brand
            )
            match.participants.set(participants)
    else:
        # PPV day
        ppv_index = ((day_number - 1) // cycle_length) % num_ppv
        current_ppv = ppv_events[ppv_index]
        all_wrestlers = list(game.wrestlers.all())

        male_wrestlers = [w for w in all_wrestlers if w.gender == 'male']
        female_wrestlers = [w for w in all_wrestlers if w.gender == 'female']

        num_matches = random.randint(4, 6)
        # Add a chance for a Royal Rumble on PPV if enough wrestlers
        ppv_match_types = match_types + (['royal_rumble'] if len(all_wrestlers) >= 30 else [])

        for _ in range(num_matches):
            wrestlers_pool = random.choice(
                [male_wrestlers, female_wrestlers]) if male_wrestlers and female_wrestlers else (
                    male_wrestlers or female_wrestlers)
            if not wrestlers_pool:
                continue

            max_participants = len(wrestlers_pool)
            valid_match_types = [
                mt for mt in ppv_match_types if participant_requirements[mt] <= max_participants
            ]
            if not valid_match_types:
                continue

            match_type = random.choice(valid_match_types)
            required_participants = participant_requirements[match_type]

            participants = random.sample(wrestlers_pool, required_participants)
            match = Match.objects.create(
                user=game.user,
                game=game,
                match_type=match_type,
                day_number=day_number,
                ppv_event=current_ppv,
                brand=random.choice(brands) if brands else None
            )
            match.participants.set(participants)


def generate_ppv_matches(game, ppv_event, day_number):
    """
    Generate matches for a PPV event based on rivalries, brands, and championships.
    If no rivalries exist, create random matches per brand and championship matches.
    Number of matches: random between 5 and 10.
    """
    match_types = ['singles', 'triple_threat', 'fatal_four_way', 'ladder_match', 'hell_in_a_cell']
    brands = list(game.brands.all())
    championships = list(game.championships.all())
    wrestlers = list(game.wrestlers.all())
    rivalries = Rivalry.objects.filter(game=game, completed=False)
    num_matches = random.randint(5, 10)

    # Step 1: Generate matches based on active rivalries
    created_matches = []
    used_wrestlers = set()  # Set of Wrestler objects

    for rivalry in rivalries:
        if len(created_matches) >= num_matches:
            break
        wrestler_one = rivalry.wrestler_one
        wrestler_two = rivalry.wrestler_two
        if wrestler_one in used_wrestlers or wrestler_two in used_wrestlers:
            continue

        match = Match.objects.create(
            user=game.user,
            game=game,
            match_type='singles',  # Rivalries are typically 1v1
            day_number=day_number,
            ppv_event=ppv_event,
            brand=rivalry.brand
        )
        match.participants.set([wrestler_one, wrestler_two])
        created_matches.append(match)
        used_wrestlers.add(wrestler_one)
        used_wrestlers.add(wrestler_two)

    # Step 2: If no rivalries or not enough matches, generate brand-based matches
    remaining_matches = num_matches - len(created_matches)
    if remaining_matches > 0 and brands:
        for brand in brands:
            if remaining_matches <= 0:
                break
            wrestler_brands = WrestlerBrand.objects.filter(brand=brand)
            # Convert used_wrestlers to a list of IDs
            used_wrestler_ids = [wrestler.id for wrestler in used_wrestlers]
            brand_wrestlers = Wrestler.objects.filter(brand_links__in=wrestler_brands).exclude(id__in=used_wrestler_ids)
            available_wrestlers = list(brand_wrestlers)
            if len(available_wrestlers) >= 2:
                num_participants = random.choice([2, 3, 4])
                participants = random.sample(available_wrestlers, min(num_participants, len(available_wrestlers)))
                match = Match.objects.create(
                    user=game.user,
                    game=game,
                    match_type=random.choice(match_types),
                    day_number=day_number,
                    ppv_event=ppv_event,
                    brand=brand
                )
                match.participants.set(participants)
                created_matches.append(match)
                used_wrestlers.update(participants)
                remaining_matches -= 1

    # Step 3: Add championship matches if not enough matches
    remaining_matches = num_matches - len(created_matches)
    if remaining_matches > 0 and championships:
        for championship in championships:
            if remaining_matches <= 0:
                break
            current_champion = championship.current_champion
            if not current_champion or current_champion in used_wrestlers:
                continue
            # Convert used_wrestlers to a list of IDs
            used_wrestler_ids = [wrestler.id for wrestler in used_wrestlers]
            challengers = Wrestler.objects.filter(
                gender=championship.gender,
                brand_links__brand__in=brands
            ).exclude(id__in=used_wrestler_ids).exclude(id=current_champion.id)
            available_challengers = list(challengers)
            if available_challengers:
                challenger = random.choice(available_challengers)
                match = Match.objects.create(
                    user=game.user,
                    game=game,
                    match_type='singles',  # Championship matches are typically 1v1
                    day_number=day_number,
                    ppv_event=ppv_event,
                    brand=random.choice(brands) if brands else None
                )
                match.participants.set([current_champion, challenger])
                created_matches.append(match)
                used_wrestlers.add(current_champion)
                used_wrestlers.add(challenger)
                remaining_matches -= 1

    # Step 4: Fill remaining matches with random wrestlers if needed
    remaining_matches = num_matches - len(created_matches)
    if remaining_matches > 0 and wrestlers:
        # Convert used_wrestlers to a list of IDs
        used_wrestler_ids = [wrestler.id for wrestler in used_wrestlers]
        available_wrestlers = Wrestler.objects.filter(id__in=[w.id for w in wrestlers]).exclude(
            id__in=used_wrestler_ids)
        available_wrestlers = list(available_wrestlers)
        while remaining_matches > 0 and len(available_wrestlers) >= 2:
            num_participants = random.choice([2, 3, 4])
            participants = random.sample(available_wrestlers, min(num_participants, len(available_wrestlers)))
            match = Match.objects.create(
                user=game.user,
                game=game,
                match_type=random.choice(match_types),
                day_number=day_number,
                ppv_event=ppv_event,
                brand=random.choice(brands) if brands else None
            )
            match.participants.set(participants)
            created_matches.append(match)
            used_wrestlers.update(participants)
            remaining_matches -= 1
            # Update available_wrestlers after adding participants
            used_wrestler_ids = [wrestler.id for wrestler in used_wrestlers]
            available_wrestlers = Wrestler.objects.filter(id__in=[w.id for w in wrestlers]).exclude(
                id__in=used_wrestler_ids)
            available_wrestlers = list(available_wrestlers)

    return created_matches