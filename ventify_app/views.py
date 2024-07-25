from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Vent, Tag, UserProfile, Therapist, UserProfile, Feedback, Report
from .serializers import VentSerializer, FeedbackSerializer, ReportSerializer, TherapistSerializer
import datetime
import uuid
from functools import wraps

def get_or_create_user_uuid(request):
    user_uuid = request.COOKIES.get('user_uuid')
    
    if user_uuid is None:
        user_uuid = uuid.uuid4()
        UserProfile.objects.create(uuid=user_uuid)
    else:
        user_uuid = uuid.UUID(user_uuid)
        UserProfile.objects.get_or_create(uuid=user_uuid)
    
    return user_uuid

def user_uuid_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_uuid = request.COOKIES.get('user_uuid')
        if not user_uuid:
            return Response({'error': 'UUID is required'}, status=status.HTTP_403_FORBIDDEN)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@api_view(['GET'])
@user_uuid_required
def vent_list(request):
    vents = Vent.objects.all().order_by('-created_at')
    serializer = VentSerializer(vents, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@user_uuid_required
def create_vent(request):
    serializer = VentSerializer(data=request.data)
    if serializer.is_valid():
        tags_data = serializer.validated_data.pop('tags')
        tags = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
        vent = serializer.save(tags=tags)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@user_uuid_required
def love_vent(request, vent_id):
    loved_vents = request.session.get('loved_vents', [])

    if vent_id in loved_vents:
        return Response({'error': 'You have already loved this vent.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        vent = Vent.objects.get(pk=vent_id)
        vent.love_count += 1
        vent.save()

        # Add vent ID to session
        loved_vents.append(vent_id)
        request.session['loved_vents'] = loved_vents

        return Response({'message': 'Vent loved successfully'})
    except Vent.DoesNotExist:
        return Response({'error': 'Vent not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@user_uuid_required
def unlove_vent(request, vent_id):
    loved_vents = request.session.get('loved_vents', [])

    if vent_id not in loved_vents:
        return Response({'error': 'You have not loved this vent.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        vent = Vent.objects.get(pk=vent_id)
        vent.love_count -= 1
        vent.save()

        # Remove vent ID from session
        loved_vents.remove(vent_id)
        request.session['loved_vents'] = loved_vents

        return Response({'message': 'Vent unloved successfully'})
    except Vent.DoesNotExist:
        return Response({'error': 'Vent not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@user_uuid_required
def create_feedback(request, therapist_name):
    therapist_name = therapist_name.replace('_', ' ')

    feedback_given = request.session.get('feedback_given', [])

    if therapist_name in feedback_given:
        return Response({'error': 'Feedback for this therapist already submitted.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        therapist = Therapist.objects.get(name=therapist_name)
    except Therapist.DoesNotExist:
        return Response({'error': 'Therapist not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = FeedbackSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(therapist=therapist)
        feedback_given.append(therapist_name)
        request.session['feedback_given'] = feedback_given
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@user_uuid_required
def report_vent(request, vent_id):
    reported_vents = request.session.get('reported_vents', [])

    if vent_id in reported_vents:
        return Response({'error': 'Vent already reported by this user.'}, status=status.HTTP_400_BAD_REQUEST)

    vent = get_object_or_404(Vent, pk=vent_id)

    report_data = {'vent': vent.id, 'reason': request.data.get('reason', 'No reason provided')}
    serializer = ReportSerializer(data=report_data)

    if serializer.is_valid():
        serializer.save()
        reported_vents.append(vent_id)
        request.session['reported_vents'] = reported_vents
        return Response({'message': 'Vent reported successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@user_uuid_required
def list_therapists(request):
    therapists = Therapist.objects.all()
    serializer = TherapistSerializer(therapists, many=True)
    return Response(serializer.data)
