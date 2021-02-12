from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Income(models.Model):
    SOURCE_OPTIONS = [
        ('SALARY', 'SALARY'),
        ('BUSINESS', 'BUSINESS'),
        ('SIDE_HUSTLE', 'SIDE_HUSTLE'),
        ('OTHERS', 'OTHERS'),
    ]
    source = models.CharField(choices=SOURCE_OPTIONS, max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.owner)+'s income'
