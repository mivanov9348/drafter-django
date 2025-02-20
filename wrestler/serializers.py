from rest_framework import serializers
from .models import Wrestler

class WrestlerSerializer(serializers.ModelSerializer):
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = Wrestler
        fields = ['id', 'name', 'age', 'overall_rating', 'image', 'gender', 'gender_display']