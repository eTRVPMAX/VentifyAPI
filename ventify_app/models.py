from django.db import models
from datetime import datetime
import uuid

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class Vent(models.Model):
    content = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    love_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    display_name = models.CharField(max_length=50, blank=True)
    anonymity_preference = models.BooleanField(default=True)

class Feedback(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)  # Unique identifier for each user profile
    therapist = models.ForeignKey('Therapist', on_delete=models.CASCADE) 
    rating = models.IntegerField()
    comments = models.TextField(blank=True)

class Report(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)  # Unique identifier for each report
    vent = models.ForeignKey(Vent, on_delete=models.CASCADE, related_name='reports')
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Report for Vent ID {self.vent.id}"

class Therapist(models.Model): 
    name = models.CharField(max_length=255)
    credentials = models.TextField()