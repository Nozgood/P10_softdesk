from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.fields import BooleanField
from users.models import User

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
        can_be_shared = attrs.get("data_can_be_shared")
        print(f"age: {age} can_be_shared:{can_be_shared}")
        if age and age < 15 and can_be_shared is True:
            raise ValidationError(
                {
                    "RGPD error":
                        "You must be at least 15 to allow data sharing",
                }
            )
        return attrs
