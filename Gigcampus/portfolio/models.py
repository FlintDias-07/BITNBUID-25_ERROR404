from django.db import models
from django.contrib.auth.models import User
from projects.models import Project

class Review(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='review')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.freelancer.username} - {self.rating} stars"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update freelancer's average rating
        self.update_freelancer_rating()
    
    def update_freelancer_rating(self):
        reviews = Review.objects.filter(freelancer=self.freelancer)
        avg_rating = sum([r.rating for r in reviews]) / len(reviews) if reviews else 0
        self.freelancer.profile.rating = round(avg_rating, 2)
        self.freelancer.profile.save()