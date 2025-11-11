from django.db import models
from django.contrib.auth.models import AbstractUser


class DatingStatuses(models.TextChoices):
    SUSITIKINEJA = 'susitikinėja', 'Susitikinėja'
    KARTAIS_SUSITINKA = "kartais susitinka", "Kartais susitinka"
    KARTAI_NE_SUSITINKA = "kartais ne susitinka", "Kartais ne susitinka"
    KOMPLIKUOTA = "kompliktuota", "Kompliktuota"
    VISKAS_AISKU = "viskas aišku", "Viskas aišku"


class Baudejas(AbstractUser):
    dating_status = models.CharField(max_length=20, choices=DatingStatuses.choices, null=True)
    favourite_color = models.CharField(max_length=100)

    def __str__(self):
        return self.username
