from django.shortcuts import render
from .models import Wrestler

def all_wrestlers(request):
    wrestlers = Wrestler.objects.all()

    filter_by = request.GET.get('filter', 'all')
    if filter_by == 'high_rating':
        wrestlers = wrestlers.order_by('-overall_rating')
    elif filter_by == 'heavyweight':
        wrestlers = wrestlers.filter(weight__gt=100)
    elif filter_by == 'lightweight':
        wrestlers = wrestlers.filter(weight__lt=80)

    return render(request, 'wrestler/wrestlers.html', {'wrestlers': wrestlers})
