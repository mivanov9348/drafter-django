from django.db import models

class Wrestler(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female')
    ]

    name = models.CharField(max_length=100, unique=True)
    age = models.IntegerField()
    overall_rating = models.IntegerField()
    image = models.ImageField(upload_to='wrestlers/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='male')

    def __str__(self):
        return self.name

class WrestlerBrand(models.Model):
    wrestler = models.ForeignKey(Wrestler, on_delete=models.CASCADE, related_name='brand_links')
    brand = models.ForeignKey('brand.Brand', on_delete=models.CASCADE, related_name='wrestler_links')

    brand_rating = models.IntegerField(default=50)

    class Meta:
        unique_together = ('wrestler', 'brand')

    def __str__(self):
        return f"{self.wrestler.name} in {self.brand.name}"
