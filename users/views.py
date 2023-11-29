from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.response import Response
from users.models import User
from users.serializers import UserSerializer
from rest_framework.parsers import JSONParser
from json import JSONDecodeError
from django.http import JsonResponse

class SignUpAPIView(APIView):
    @staticmethod
    def get(request):
        return render(
            request,
            template_name='user.html',
        )

    @staticmethod
    def post(request):
        try:
            data = JSONParser().parse(request)
            print(f"data : {data}")
            serializer = UserSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        except JSONDecodeError:
            return JsonResponse(
                {
                    "response": "error",
                    "message": "JSON decoding error"
                },
                status=400)


class LoginAPIView(APIView):
    @staticmethod
    def get(request):
        pass
