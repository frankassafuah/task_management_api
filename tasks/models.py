from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from auth_app.models import User

# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)

class Task(models.Model):
    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=10)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='Pending')
    completed_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)

    def mark_complete(self):
        self.status = 'Completed'
        self.completed_at = timezone.now()
        self.save()

    def mark_incomplete(self):
        self.status = 'Pending'
        self.completed_at = None
        self.save()
