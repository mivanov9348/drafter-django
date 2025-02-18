import os
import django
from wrestler.models import Wrestler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drafter.settings')
django.setup()

wrestlers_data = [
    {"name": "John Cena", "age": 46, "weight": 114.0, "height": 1.85, "overall_rating": 95},
    {"name": "The Rock", "age": 51, "weight": 118.0, "height": 1.96, "overall_rating": 97},
    {"name": "Stone Cold Steve Austin", "age": 59, "weight": 114.0, "height": 1.88, "overall_rating": 96},
    {"name": "Roman Reigns", "age": 38, "weight": 120.0, "height": 1.91, "overall_rating": 96},
    {"name": "Brock Lesnar", "age": 46, "weight": 130.0, "height": 1.91, "overall_rating": 98},
    {"name": "Triple H", "age": 54, "weight": 118.0, "height": 1.93, "overall_rating": 97},
    {"name": "Shawn Michaels", "age": 58, "weight": 102.0, "height": 1.80, "overall_rating": 95},
    {"name": "Undertaker", "age": 58, "weight": 136.0, "height": 2.08, "overall_rating": 98},
    {"name": "Kurt Angle", "age": 55, "weight": 108.0, "height": 1.83, "overall_rating": 94},
    {"name": "Edge", "age": 50, "weight": 113.0, "height": 1.96, "overall_rating": 96},
]

for wrestler in wrestlers_data:
    obj, created = Wrestler.objects.get_or_create(
        name=wrestler["name"],
        defaults={
            "age": wrestler["age"],
            "weight": wrestler["weight"],
            "height": wrestler["height"],
            "overall_rating": wrestler["overall_rating"]
        }
    )
    if created:
        print(f"Added {wrestler['name']} to the database.")
    else:
        print(f"{wrestler['name']} already exists.")

print("✅ Wrestlers added successfully!")
