from django.contrib.auth.models import AbstractUser
from django.db import models


# Append custom fields in django buildin user
class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    designation = models.CharField(max_length=100, default="User")
    access_level = models.PositiveIntegerField(default=0)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class Task(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
    ]

    TASK_TYPES = [
        ("BUG", "Bug"),
        ("FEATURE", "Feature"),
        ("IMPROVEMENT", "Improvement"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # Update datetime to track each updation like assigned to user or status change.
    updated_at = models.DateTimeField(auto_now=True)
    task_type = models.CharField(max_length=20, choices=TASK_TYPES, default="FEATURE")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    # Used many-to-many relationship to assigned user to maintain relationship that the task can be assigned to multiple users, and a user can have multiple tasks.
    assigned_users = models.ManyToManyField(User, related_name="tasks")

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"
