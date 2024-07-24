from django.contrib import admin
from .models import (
    Tag,
    Vent,
    UserProfile,
    Feedback,
    Report,
    Therapist,
)

admin.site.register(Tag)
admin.site.register(Vent)
admin.site.register(UserProfile)
admin.site.register(Feedback)
admin.site.register(Report)
admin.site.register(Therapist)
