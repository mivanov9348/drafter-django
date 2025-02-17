from django.conf import settings
from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='brands'
    )

    class Meta:
        unique_together = ('owner', 'name')

    def __str__(self):
        return f"{self.name} (Owner: {self.owner.username})"
