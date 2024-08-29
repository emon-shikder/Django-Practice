from django.db import models
from musician.models import Musician

class Album(models.Model):
    album_name = models.CharField(max_length=100)
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    release_date = models.DateField()

    ratings = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )

    rating = models.IntegerField(choices = ratings)

    def __str__(self):
        return self.album_name