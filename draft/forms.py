from django import forms
from .models import Draft
from brand.models import Brand

class DraftForm(forms.ModelForm):
    brands = forms.ModelMultipleChoiceField(
        queryset=Brand.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Draft
        fields = ['name', 'brands']
