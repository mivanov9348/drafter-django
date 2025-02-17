from django.shortcuts import render, get_object_or_404
from .models import Brand
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BrandForm

def brand_list(request):
    brands = Brand.objects.filter(owner=request.user).prefetch_related('wrestlers')
    return render(request, 'brand/brands.html', {'brands': brands})

@login_required
def brand_create(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            brand = form.save(commit=False)
            brand.owner = request.user
            brand.save()
            return redirect('brand:brand_list')
    else:
        form = BrandForm()
    return render(request, 'brand/brand_create_modal.html', {'form': form})

@login_required
def brand_delete(request, pk):
    brand = get_object_or_404(Brand, pk=pk, owner=request.user)
    if request.method == 'POST':
        brand.delete()
        return redirect('brand:brand_list')
    return render(request, 'brand/brand_confirm_delete.html', {'brand': brand})