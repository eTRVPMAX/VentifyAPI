import uuid
from .models import UserProfile

class UUIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user_uuid = request.COOKIES.get('user_uuid')
        if not user_uuid:
            user_uuid = uuid.uuid4()
            UserProfile.objects.create(uuid=user_uuid)
            response.set_cookie('user_uuid', user_uuid)
        return response
