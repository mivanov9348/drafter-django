import random

from manager_game.models import Rivalry
from matches.models import Match
from wrestler.models import Wrestler, WrestlerBrand


def get_game_days(game):
    brands = list(game.brands.all())
    ppv_events = list(game.ppv_events.all().order_by('date'))
    num_brands = len(brands)
    num_ppv = len(ppv_events)
    cycle_length = num_brands + 1  # Брой brands + 1 за PPV

    total_days = cycle_length * num_ppv
    days = []
    for day_number in range(1, total_days + 1):
        position = (day_number - 1) % cycle_length
        if position < num_brands:
            event = brands[position].name
        else:
            ppv_index = ((day_number - 1) // cycle_length) % num_ppv
            event = ppv_events[ppv_index].name
        days.append({'day_number': day_number, 'event': event})

    return days

