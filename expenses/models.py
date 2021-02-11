from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Expenses(models.Model):
    CATEGORY_OPTIONS = [
        ('ONLINE_SERVICES', 'ONLINE_SERVICES'),
        ('RENT', 'RENT'),
        ('TRAVEL', 'TRAVEL'),
        ('FOOD', 'FOOD'),
        ('OTHERS', 'OTHERS'),
    ]
    category = models.CharField(choices=CATEGORY_OPTIONS, max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
