import random
from datetime import timedelta

from matches.models import Match
from wrestler.models import Wrestler


def distribute_matches_for_brands(game, brands, calendar, user):
    """
    Разпределя мачове за всеки brand ден в календара на играта.

    :param game: Инстанция на Game
    :param brands: Списък с Brand обекти
    :param calendar: Инстанция на Calendar
    :param user: Потребител, който притежава играта
    """
    num_brands = len(brands)
    ppv_events = list(game.ppv_events.all().order_by('date'))
    num_ppv = len(ppv_events)
    cycle_length = num_brands + 1  # Брой brands + 1 за PPV
    total_days = cycle_length * num_ppv  # Общ брой дни за сезона

    match_types = ['singles', 'triple_threat', 'fatal_four_way']

    for day_number in range(1, total_days + 1):
        position = (day_number - 1) % cycle_length
        if position < num_brands:
            current_brand = brands[position]
            wrestlers = list(Wrestler.objects.filter(brand_links__brand=current_brand))

            if len(wrestlers) < 2:
                continue

            num_matches = random.randint(1, 3)
            for _ in range(num_matches):
                num_participants = random.choice([2, 3, 4])
                participants = random.sample(wrestlers, min(num_participants, len(wrestlers)))
                winner = random.choice(participants)

                match_date = calendar.start_date + timedelta(days=day_number - 1)

                match = Match.objects.create(
                    user=user,  # Задаваме потребителя
                    match_type=random.choice(match_types),
                    winner=winner,
                    brand=current_brand,
                    date=match_date
                )
                match.participants.set(participants)