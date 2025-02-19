from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Brand
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BrandForm

def brand_list(request):
    brands = Brand.objects.filter(owner=request.user).prefetch_related('wrestler_links')
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
def delete_brand(request, brand_id):
    if request.method == "POST":
        try:
            brand = get_object_or_404(Brand, id=brand_id, owner=request.user)
            brand.delete()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    return JsonResponse({"success": False, "error": "Invalid request method."}, status=400)