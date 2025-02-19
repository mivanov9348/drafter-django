from django.db import models

class Wrestler(models.Model):
    name = models.CharField(max_length=100, unique=True)
    alias = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField()
    overall_rating = models.IntegerField()  # Глобален рейтинг
    image = models.ImageField(upload_to='wrestlers/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)

    enemies = models.ManyToManyField('self', symmetrical=False, related_name='rivalries', blank=True)

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
