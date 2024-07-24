from rest_framework import serializers
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
    class Meta:
        model = Therapist
        fields = ('id', 'name', 'credentials')
