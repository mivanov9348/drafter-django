from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Wrestler
from .serializers import WrestlerSerializer


@api_view(['GET'])
def wrestlers_api(request):
    filter_by = request.GET.get('filter', 'all')
    page = int(request.GET.get('page', 1))
    per_page = 10  # Кечисти на страница

    wrestlers = Wrestler.objects.all()

    if filter_by == 'male':
        wrestlers = wrestlers.filter(gender='male')
    elif filter_by == 'female':
        wrestlers = wrestlers.filter(gender='female')
    elif filter_by == 'high_rating':
        wrestlers = wrestlers.order_by('-overall_rating')
    elif filter_by == 'age':
        wrestlers = wrestlers.order_by('age')
    elif filter_by == 'name':
        wrestlers = wrestlers.order_by('name')

    start = (page - 1) * per_page
    end = start + per_page
    paginated_wrestlers = wrestlers[start:end]

    serializer = WrestlerSerializer(paginated_wrestlers, many=True)
    return Response({
        'wrestlers': serializer.data,
        'has_more': end < wrestlers.count()
    })

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
