# Vendor
from django.http.response import JsonResponse
from django.utils.deprecation import MiddlewareMixin

# Local
from .models import User
from .services import verify_token


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """Authorization token from header"""
        auth_header = request.headers.get("Authorization")
        if auth_header is None:
            return

        token = auth_header.split()
        if len(token) != 2:
            return JsonResponse(data={"error_code": "INVALID_AUTH_HEADER"}, status=400)

        verified_token = verify_token(token[1], "access")

        if not verified_token:
            return JsonResponse(data={"error_code": "INVALID_TOKEN"}, status=401)

        try:
            user = User.objects.get(id=verified_token["user_id"])
        except User.DoesNotExist:
            return JsonResponse(data={"error_code": "USER_NOT_FOUND"}, status=404)

        request.user = user


class DisableCSRF(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, "_dont_enforce_csrf_checks", True)
