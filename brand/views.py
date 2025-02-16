from django.shortcuts import render
from .models import Brand

def brand_list(request):
    brands = Brand.objects.all()
    return render(request, 'brand/list.html', {'brands': brands})
