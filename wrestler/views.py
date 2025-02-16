from django.shortcuts import render
from .models import Wrestler

def wrestler_list(request):
    wrestlers = Wrestler.objects.all()
    return render(request, 'wrestler/list.html', {'wrestlers': wrestlers})
