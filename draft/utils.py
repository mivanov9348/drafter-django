from django.db import models
from django.db.models import Count, Avg

from draft.models import DraftPick
from wrestler.models import Wrestler, WrestlerBrand


def smart_wrestler_pick(draft, brand):
    picked_wrestlers = DraftPick.objects.filter(draft=draft).values_list('wrestler_id', flat=True)
    available_wrestlers = Wrestler.objects.exclude(id__in=picked_wrestlers)

    if not available_wrestlers.exists():
        return None

    brand_picks = DraftPick.objects.filter(draft=draft, brand=brand)
    brand_wrestlers = brand_picks.values_list('wrestler', flat=True)
    brand_wrestler_details = Wrestler.objects.filter(id__in=brand_wrestlers)

    gender_counts = brand_wrestler_details.aggregate(
        male_count=Count('id', filter=models.Q(gender='male')),
        female_count=Count('id', filter=models.Q(gender='female'))
    )
    male_count = gender_counts['male_count'] or 0
    female_count = gender_counts['female_count'] or 0

    brand_ratings = WrestlerBrand.objects.filter(brand=brand, wrestler__in=brand_wrestlers).aggregate(
        Avg('brand_rating')
    )
    avg_brand_rating = brand_ratings['brand_rating__avg'] or 0

    if male_count > female_count + 1:
        candidates = available_wrestlers.filter(gender='female')
    elif female_count > male_count + 1:
        candidates = available_wrestlers.filter(gender='male')
    else:
        candidates = available_wrestlers

    if not candidates.exists():
        candidates = available_wrestlers

    wrestler_brand_ratings = WrestlerBrand.objects.filter(
        brand=brand, wrestler__in=candidates
    ).select_related('wrestler')

    if wrestler_brand_ratings.exists():
        if avg_brand_rating > 0:
            sorted_candidates = sorted(
                wrestler_brand_ratings,
                key=lambda wb: wb.brand_rating,
                reverse=True
            )[:3]
            chosen_wb = min(
                sorted_candidates,
                key=lambda wb: abs(wb.brand_rating - avg_brand_rating),
                default=None
            )
            chosen = chosen_wb.wrestler if chosen_wb else None
        else:
            chosen = wrestler_brand_ratings.order_by('-brand_rating').first().wrestler
    else:
        if avg_brand_rating > 0:  # Това няма да е вярно, но за консистентност
            sorted_candidates = candidates.order_by('-overall_rating')[:3]
            chosen = min(
                sorted_candidates,
                key=lambda w: abs(w.overall_rating - avg_brand_rating),
                default=None
            )
        else:
            chosen = candidates.order_by('-overall_rating').first()

    return chosen