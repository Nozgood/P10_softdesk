from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.fields import BooleanField
from users.models import User, LoginUser

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

    def validate(self, attrs):
        age = attrs.get("age")
        if age < 15:
            raise ValidationError(
                {
                    "RGPD error":
                        "You must be at least 15 to be allow to create an account",
                }
            )
        return attrs

class LoginSerializer(ModelSerializer):
    class Meta:
        model = LoginUser
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