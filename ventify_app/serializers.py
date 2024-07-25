from rest_framework import serializers
from django.db import models
from rest_framework.serializers import SlugRelatedField
from .models import (
    Tag,
    Vent,
    UserProfile,
    Feedback,
    Report,
    Therapist,
)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class VentSerializer(serializers.ModelSerializer):
    tags = SlugRelatedField(many=True, slug_field='name', queryset=Tag.objects.all())
    class Meta:
        model = Vent
        fields = ('id', 'content', 'tags', 'love_count', 'created_at')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('display_name', 'anonymity_preference')


class FeedbackSerializer(serializers.ModelSerializer):
    therapist_name = serializers.ReadOnlyField(source='therapist.name')
    class Meta:
        model = Feedback
        fields = ['id', 'therapist_name', 'rating', 'comments']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class TherapistSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()  # Add this line

    class Meta:
        model = Therapist
        fields = ('id', 'name', 'credentials', 'average_rating')

    def get_average_rating(self, obj):
        feedbacks = Feedback.objects.filter(therapist=obj)
        if feedbacks.exists():
            return feedbacks.aggregate(models.Avg('rating'))['rating__avg']
        return None
