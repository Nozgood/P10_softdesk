from rest_framework.serializers import ModelSerializer
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
