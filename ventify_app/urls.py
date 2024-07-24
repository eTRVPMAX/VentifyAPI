from django.urls import path
from . import views

urlpatterns = [
    path('vents/', views.vent_list, name='vent_list'),
    path('vents/create/', views.create_vent, name='create_vent'),
    path('vents/<int:vent_id>/love/', views.love_vent, name='love_vent'),
    path('therapists/', views.list_therapists, name='therapists-list'),
    path('feedback/<slug:therapist_name>/', views.create_feedback, name='create_feedback'),
    path('vents/<int:vent_id>/report/', views.report_vent, name='report_vent'),
]
