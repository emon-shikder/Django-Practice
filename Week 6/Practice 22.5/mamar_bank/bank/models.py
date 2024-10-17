from django.db import models

class BankModel(models.Model):
    is_bankrupt = models.BooleanField(default=False)

    def __str__(self):
        return f"Bank Status: {'Bankrupt' if self.is_bankrupt else 'Operational'}"
