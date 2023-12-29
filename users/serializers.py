from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    CharField
)
from rest_framework.fields import BooleanField
from users.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

class UserSerializer(ModelSerializer):
    can_be_contacted = BooleanField(required=True)
    data_can_be_shared = BooleanField(required=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'password',
            'age',
            'can_be_contacted',
            'data_can_be_shared'
        ]

    @staticmethod
    def validate_password(value):
        validate_password(value)
        return value

    def validate(self, attrs):
        age = attrs.get("age")
        if age < 15:
            raise ValidationError(
                {
                    "RGPD error":
                        "You must be at least 15 to be "
                        "allow to create an account",
                }
            )
        return attrs

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return User.objects.create(**validated_data)

class LoginSerializer(ModelSerializer):
    username = CharField(max_length=150)
    password = CharField(max_length=128)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
        ]

    def validate(self, attrs):
        if len(attrs["password"]) == 0 or len(attrs["username"]) == 0:
            raise ValidationError(
                {
                    "Error": "Please filled a username and a password to login"
                }
            )
        return attrs
