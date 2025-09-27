from django.db import models
from projects.models import Bid

class Escrow(models.Model):
    STATUS_CHOICES = [
        ('held', 'Held'),
        ('released', 'Released'),
    ]
    
    bid = models.OneToOneField(Bid, on_delete=models.CASCADE, related_name='escrow')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='held')
    created_at = models.DateTimeField(auto_now_add=True)
    released_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Escrow for {self.bid.project.title} - ${self.amount}"