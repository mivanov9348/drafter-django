import random
from datetime import timedelta

from matches.models import Match
from wrestler.models import Wrestler


def distribute_matches_for_brands(game, brands, calendar, user):

    num_brands = len(brands)
    ppv_events = list(game.ppv_events.all().order_by('date'))
    num_ppv = len(ppv_events)
    cycle_length = num_brands + 1  # Брой brands + 1 за PPV
    total_days = cycle_length * num_ppv  # Общ брой дни за сезона

    match_types = ['singles', 'triple_threat', 'fatal_four_way']

    for day_number in range(1, total_days + 1):
        position = (day_number - 1) % cycle_length
        if position < num_brands:  # Ако е ден за brand (не PPV)
            current_brand = brands[position]
            wrestlers = list(Wrestler.objects.filter(brand_links__brand=current_brand))

            if len(wrestlers) < 10:
                continue

            used_wrestlers = set()
            for _ in range(5):
                available_wrestlers = [w for w in wrestlers if w not in used_wrestlers]
                if len(available_wrestlers) < 2:
                    break

                num_participants = random.choice([2, 3, 4])
                num_participants = min(num_participants, len(available_wrestlers))

                participants = random.sample(available_wrestlers, num_participants)
                winner = random.choice(participants)

                used_wrestlers.update(participants)

                match_date = calendar.start_date + timedelta(days=day_number - 1)

                match = Match.objects.create(
                    user=user,
                    match_type=random.choice(match_types),
                    winner=winner,
                    brand=current_brand,
                    date=match_date
                )
                match.participants.set(participants)

    return True