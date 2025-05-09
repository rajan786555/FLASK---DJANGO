from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class MenuItem(models.Model):
    VEG = 'veg'
    NON_VEG = 'non-veg'
    CATEGORY_CHOICES = [
        (VEG, 'Vegetarian'),
        (NON_VEG, 'Non-Vegetarian'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    image = models.ImageField(upload_to='menu_images/')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    badge = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.name


class ContactForm(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"