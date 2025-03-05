from django.db import transaction
from datetime import timedelta
import random
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
    match_types = ['singles', 'triple_threat', 'fatal_four_way', 'ladder_match']

    if position < num_brands:
        # Brand day
        current_brand = brands[position]
        # Get wrestlers for the current brand only
        wrestler_brands = WrestlerBrand.objects.filter(brand=current_brand)
        all_wrestlers = Wrestler.objects.filter(brand_links__in=wrestler_brands).distinct()

        # Separate male and female wrestlers
        male_wrestlers = list(all_wrestlers.filter(gender='male'))
        female_wrestlers = list(all_wrestlers.filter(gender='female'))

        num_matches = random.randint(3, 5)  # Generate 3-5 matches for the brand
        for _ in range(num_matches):
            # Randomly choose gender pool for this match
            wrestlers_pool = random.choice(
                [male_wrestlers, female_wrestlers]) if male_wrestlers and female_wrestlers else (
                        male_wrestlers or female_wrestlers)
            if not wrestlers_pool:  # Skip if no wrestlers available
                continue

            num_participants = random.choice([2, 3, 4])
            available_participants = min(num_participants, len(wrestlers_pool))
            if available_participants < 2:  # Need at least 2 participants
                continue

            participants = random.sample(wrestlers_pool, available_participants)
            match = Match.objects.create(
                user=game.user,
                game=game,
                match_type=random.choice(match_types),
                day_number=day_number,
                brand=current_brand
            )
            match.participants.set(participants)
    else:
        # PPV day
        ppv_index = ((day_number - 1) // cycle_length) % num_ppv
        current_ppv = ppv_events[ppv_index]
        # For PPV, allow wrestlers from all brands but still separate by gender
        all_wrestlers = list(game.wrestlers.all())

        # Separate male and female wrestlers
        male_wrestlers = [w for w in all_wrestlers if w.gender == 'male']
        female_wrestlers = [w for w in all_wrestlers if w.gender == 'female']

        num_matches = random.randint(4, 6)  # More matches for PPV
        for _ in range(num_matches):
            # Randomly choose gender pool for this match
            wrestlers_pool = random.choice(
                [male_wrestlers, female_wrestlers]) if male_wrestlers and female_wrestlers else (
                        male_wrestlers or female_wrestlers)
            if not wrestlers_pool:  # Skip if no wrestlers available
                continue

            num_participants = random.choice([2, 3, 4])
            available_participants = min(num_participants, len(wrestlers_pool))
            if available_participants < 2:  # Need at least 2 participants
                continue

            participants = random.sample(wrestlers_pool, available_participants)
            match = Match.objects.create(
                user=game.user,
                game=game,
                match_type=random.choice(match_types),
                day_number=day_number,
                ppv_event=current_ppv,
                brand=random.choice(brands) if brands else None
            )
            match.participants.set(participants)

def distribute_matches_for_brands(game, brands, calendar, user):
    num_brands = len(brands)
    ppv_events = list(game.ppv_events.all().order_by('date'))
    num_ppv = len(ppv_events)
    cycle_length = num_brands + 1  # Брой brands + 1 за PPV
    total_days = cycle_length * num_ppv  # Общ брой дни за сезона

    match_types = ['singles', 'triple_threat', 'fatal_four_way']
    ppv_day_map = {ppv.date: ppv for ppv in ppv_events}  # Карта за бърз достъп до PPV по дата

    with transaction.atomic():  # Уверяваме се, че всичко се записва или нищо
        for day_number in range(1, total_days + 1):
            position = (day_number - 1) % cycle_length
            day_date = calendar.start_date + timedelta(days=day_number - 1)  # Реална дата за PPV
            ppv_event = ppv_day_map.get(day_date)  # Проверяваме дали е PPV ден

            if position < num_brands and not ppv_event:  # Ден за бранд
                current_brand = brands[position]
                wrestler_brands = WrestlerBrand.objects.filter(brand=current_brand)
                male_wrestlers = list(Wrestler.objects.filter(brand_links__in=wrestler_brands, gender='male'))
                female_wrestlers = list(Wrestler.objects.filter(brand_links__in=wrestler_brands, gender='female'))

                print(f"Day {day_number}, Brand: {current_brand.name}, Males: {len(male_wrestlers)}, Females: {len(female_wrestlers)}")

                if len(male_wrestlers) < 2 and len(female_wrestlers) < 2:
                    print(f"Skipping day {day_number} for {current_brand.name}: Not enough wrestlers")
                    continue

                matches_created = 0
                for _ in range(5):
                    if len(male_wrestlers) >= 2 and len(female_wrestlers) >= 2:
                        wrestlers = random.choice([male_wrestlers, female_wrestlers])
                    elif len(male_wrestlers) >= 2:
                        wrestlers = male_wrestlers
                    elif len(female_wrestlers) >= 2:
                        wrestlers = female_wrestlers
                    else:
                        break

                    used_wrestlers = set()
                    available_wrestlers = [w for w in wrestlers if w not in used_wrestlers]
                    if len(available_wrestlers) < 2:
                        print(f"Stopped at {matches_created} matches for day {day_number}: Not enough available wrestlers")
                        break

                    num_participants = random.choice([2, 3, 4])
                    num_participants = min(num_participants, len(available_wrestlers))

                    participants = random.sample(available_wrestlers, num_participants)
                    used_wrestlers.update(participants)

                    try:
                        match = Match.objects.create(
                            user=user,
                            game=game,  # Свързваме мача с играта
                            match_type=random.choice(match_types),
                            brand=current_brand,
                            day_number=day_number,  # Задаваме конкретния ден
                            ppv_event=None
                        )
                        match.participants.set(participants)
                        matches_created += 1
                        print(f"Created match {matches_created} for day {day_number}, brand {current_brand.name}")
                    except Exception as e:
                        print(f"Error creating match for day {day_number}: {str(e)}")
                        break

            elif ppv_event:  # PPV ден
                print(f"Day {day_number}, PPV: {ppv_event.name}")
                all_wrestlers = Wrestler.objects.filter(brand_links__brand__in=brands).distinct()
                if all_wrestlers.count() >= 2:
                    participants = random.sample(list(all_wrestlers), min(4, all_wrestlers.count()))
                    try:
                        match = Match.objects.create(
                            user=user,
                            game=game,  # Свързваме с играта
                            match_type=random.choice(match_types),
                            brand=None,
                            day_number=day_number,
                            ppv_event=ppv_event
                        )
                        match.participants.set(participants)
                        print(f"Created PPV match for {ppv_event.name} on day {day_number}")
                    except Exception as e:
                        print(f"Error creating PPV match for day {day_number}: {str(e)}")

    return True