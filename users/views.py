from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from users.models import User
from users.serializers import UserSerializer, LoginSerializer
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

class DeleteUserAPIView(APIView):
    def delete(self, request):
        return JsonResponse(
            {
                "response": "error",
                "message": "delete not implemented",
            },
            status=400)


class UpdateUserAPIView(APIView):
    def put(self, request):
        print("hello bro")
        return JsonResponse(
            {
                "response": "error",
                "message": "put not implemented",
            },
            status=400)


class LoginAPIView(APIView):
    @staticmethod
    def post(request):
        try:
            data = JSONParser().parse(request)
            print(f"data : {data}")
            serializer = LoginSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                user = get_object_or_404(
                    User,
                    username=serializer.data["username"],
                    password=serializer.data["password"]
                )
                print(f'user: {user}')
                return JsonResponse(
                {
                    "user": user.__str__(),
                    "message": "you are connected"
                },
                status=400)

        except JSONDecodeError:
            return JsonResponse(
                {
                    "response": "error",
                    "message": "JSON decoding error"
                },
                status=400)

