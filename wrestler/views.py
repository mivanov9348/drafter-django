from django.shortcuts import render
from .models import Wrestler


def all_wrestlers(request):
    wrestlers = Wrestler.objects.all()

    filter_by = request.GET.get('filter', 'all')

    if filter_by == 'male':
        wrestlers = wrestlers.filter(gender='male')
    elif filter_by == 'female':
        wrestlers = wrestlers.filter(gender='female')

    if filter_by == 'high_rating':
        wrestlers = wrestlers.order_by('-overall_rating')
    elif filter_by == 'age':
        wrestlers = wrestlers.order_by('age')
    elif filter_by == 'name':
        wrestlers = wrestlers.order_by('name')

    return render(request, 'wrestler/wrestlers.html', {'wrestlers': wrestlers})
