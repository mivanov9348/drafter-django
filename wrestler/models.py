from django.db import models

class Wrestler(models.Model):
    name = models.CharField(max_length=100, unique=True)
    age = models.IntegerField()
    overall_rating = models.IntegerField()
    image = models.ImageField(upload_to='wrestlers/', null=True, blank=True)
    brand = models.ForeignKey(
        'brand.brand',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='wrestlers'
    )

    def __str__(self):
        return self.name
