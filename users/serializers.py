from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    CharField
)
from rest_framework.fields import BooleanField
from users.models import User
from django.contrib.auth.hashers import make_password
class UserSerializer(ModelSerializer):

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

    can_be_contacted = BooleanField(
        required=True
    )

    data_can_be_shared = BooleanField(
        required=True
    )

    @staticmethod
    def validate_password(value):
        return make_password(value)

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
        print("login validator")
        if len(attrs["password"]) == 0 or len(attrs["username"]) == 0:
            raise ValidationError(
                {
                    "Error": "Please filled a username and a password to login"
                }
            )
        return attrs
