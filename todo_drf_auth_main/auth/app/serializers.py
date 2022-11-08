from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

# Local
from .models import User, Skill, Education, Work


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ("id", "name", "value")


class SkillCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        super().create(validated_data)


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ("id", "who", "where", "when", "desc")


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ("id", "who", "where", "when", "desc")


class UserSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(allow_null=True)

    class Meta:
        model = User
        fields = ["id", "username", "skills", "is_superuser"]


class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, required=True)
    new_password = serializers.CharField(max_length=128, required=True)

    def validate_new_password(self, attr):
        validate_password(attr)
        return attr

    def validate_passwords(self, attrs):
        if attrs["old_password"] == attrs["new_password"]:
            raise ValidationError("Пароли совпадают", code="match")

    def validate(self, attrs):
        self.validate_passwords(attrs)
        return attrs


class LoginSerializer(serializers.Serializer):
    """Login to system"""

    username = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(max_length=128, required=True)


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=4000, required=True)


class VerifySerializer(serializers.Serializer):
    token = serializers.CharField(max_length=4000, required=True)


class RegisterSerializer(serializers.ModelSerializer):
    """Registration user"""

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "password", "username"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, attr):
        validate_password(attr)
        return attr

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
