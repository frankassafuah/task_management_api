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
    due_date = models.DateField()  # Task due date (validation will ensure this is in the future)
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=10) # Task priority: Low, Medium, or High
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='Pending') # Task status: Pending or Completed
    completed_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE) # Each task is linked to a user

    def mark_complete(self):
        self.status = 'Completed'
        self.completed_at = timezone.now() # Timestamp when the task is marked as completed
        self.save()

    def mark_incomplete(self):
        self.status = 'Pending'
        self.completed_at = None
        self.save()

    def __str__(self):
        return self.title  # For better representation in Django admin