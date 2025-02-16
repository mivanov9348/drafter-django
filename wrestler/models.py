from django.db import models

class Wrestler(models.Model):
    name = models.CharField(max_length=100, unique=True)
    age = models.IntegerField()
    weight = models.FloatField()
    height = models.FloatField()
    overall_rating = models.IntegerField()
    image = models.ImageField(upload_to='wrestlers/', null=True, blank=True)

    def __str__(self):
        return self.name
