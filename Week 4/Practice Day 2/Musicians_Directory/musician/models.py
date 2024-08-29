from django.db import models

class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11)

    INSTRUMENT_TYPES = (
        ('guitar', 'Guitar'),
        ('piano', 'Piano'),
        ('drums', 'Drums'),
        ('violin', 'Violin'),
        ('saxophone', 'Saxophone'),
    )

    instrument_type = models.CharField(max_length=20, choices=INSTRUMENT_TYPES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"