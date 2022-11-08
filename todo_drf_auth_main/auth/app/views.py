from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from . import serializers, services
from .models import User, Skill, Education, Work


class UserView(ReadOnlyModelViewSet):
    """Common view for users"""

    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class LoginView(GenericViewSet):
    serializer_class = serializers.LoginSerializer
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"error_code": "VALIDATION_ERROR", "detail": serializer.errors},
                status=400,
            )

        user = authenticate(
            request=request,
            username=serializer.data.get("username"),
            password=serializer.data.get("password"),
        )

        if user:
            check_user = services.check_user(user)
            if check_user != "OK":
                return Response(
                    {"error_code": "CHECK_USER_ERROR", "detail": check_user}, status=401
                )

            access = services.generate_token(user, settings.JWT_ACCESS_TOKEN_LIFETIME)

            refresh = services.generate_token(
                user, settings.JWT_REFRESH_TOKEN_LIFETIME, "refresh"
            )

            return Response({"access": access, "refresh": refresh})
        else:
            return Response(
                {
                    "error_code": "AUTHENTICATION_FAILED",
                    "detail": "Error login or password",
                },
                status=403,
            )


class RefreshTokenView(GenericViewSet):
    serializer_class = serializers.RefreshSerializer
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        """Refresh access token"""
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"error_code": "VALIDATION_ERROR", "detail": serializer.errors},
                status=400,
            )

        verified_token = services.verify_token(
            serializer.data.get("refresh"), "refresh"
        )
        if not verified_token:
            return Response({"error_code": "INVALID_TOKEN"}, status=401)

        try:
            user = User.objects.get(id=verified_token["user_id"])
        except User.DoesNotExist:
            return Response(
                {"error_code": "USER_NOT_FOUND", "detail": "User not found or created"},
                status=404,
            )
        access = services.generate_token(user, settings.JWT_ACCESS_TOKEN_LIFETIME)

        return Response({"access": access})


class VerifyView(GenericViewSet):
    permission_classes = ()
    serializer_class = serializers.VerifySerializer

    def verify(self, request, *args, **kwargs):
        """Check token for verification"""
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"error_code": "VALIDATION_ERROR", "detail": serializer.errors},
                status=400,
            )

        verified_token = services.verify_token(serializer.data.get("token"), "access")
        if not verified_token:
            return Response({"error_code": "INVALID_TOKEN"}, status=401)

        return Response(verified_token)


class SkillView(GenericViewSet):
    permission_classes = ()
    serializer_class = serializers.SkillSerializer

    def get_skills(self, request, *args, **kwargs):
        user_id = request.GET.get("user_id")
        skills = Skill.objects.filter(user_id=user_id)
        serializer = self.get_serializer(skills, many=True)
        return Response(serializer.data)

    def create_skill(self, request, *args, **kwargs):
        data = request.data
        skill = Skill.objects.create(
            user_id=data["user_id"],
            name=data["name"],
            value=data["value"]
        )
        ser = self.get_serializer(skill)
        return Response(ser.data)


class WorkView(GenericViewSet):
    permission_classes = ()
    serializer_class = serializers.WorkSerializer

    def get_skills(self, request, *args, **kwargs):
        user_id = request.GET.get("user_id")
        skills = Work.objects.filter(user_id=user_id)
        serializer = self.get_serializer(skills, many=True)
        return Response(serializer.data)


class EducationView(GenericViewSet):
    permission_classes = ()
    serializer_class = serializers.EducationSerializer

    def get_skills(self, request, *args, **kwargs):
        user_id = request.GET.get("user_id")
        skills = Education.objects.filter(user_id=user_id)
        serializer = self.get_serializer(skills, many=True)
        return Response(serializer.data)


class RegisterView(GenericViewSet):
    permission_classes = ()
    serializer_class = serializers.RegisterSerializer

    def create(self, request, *args, **kwargs):
        """Register new user"""
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        print(serializer)

        if not serializer.is_valid():
            return Response(
                {"error_code": "VALIDATION_ERROR", "detail": serializer.errors},
                status=400,
            )
        serializer.save()

        return Response(serializer.data, status=201)


class PasswordView(GenericViewSet):
    serializer_class = serializers.PasswordSerializer

    def change(self, request, *args, **kwargs):
        """Change password"""
        if not request.user.check_password(request.data.get("old_password")):
            return Response(
                {"error_code": "INCORRECT_PASSWORD", "detail": "Incorrect password"},
                status=403,
            )

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error_code": "VALIDATION_ERROR", "detail": serializer.errors},
                status=400,
            )

        services.change_password(request.user, serializer.data.get("new_password"))
        return Response(status=204)
