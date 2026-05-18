from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):

    CATEGORY_CHOICES = [
        ('starwars', 'LEGO Star Wars'),
        ('icons', 'LEGO Icons'),
        ('technic', 'LEGO Technic'),
        ('ideas', 'LEGO Ideas'),
        ('ninjago', 'LEGO Ninjago'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='starwars')

    def __str__(self):
        return self.name


        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)



