from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from users.models import User
from users.serializers import UserSerializer, LoginSerializer
from rest_framework.parsers import JSONParser
from json import JSONDecodeError
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth.hashers import check_password


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
    def post(request):
        try:
            data = JSONParser().parse(request)
            serializer = LoginSerializer(data=data)
            if not serializer.is_valid():
                return JsonResponse(
                    {
                        "response": "error",
                        "message": "JSON decoding error"
                    },
                    status=400
                )
            user = get_object_or_404(
                User,
                username=serializer.data["username"],
            )
            if not check_password(
                    serializer.data["password"],
                    user.password
            ):
                return JsonResponse(
                    {
                        "response": "error",
                        "message": "incorrect password"
                    },
                    status=401
                )
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)
            return JsonResponse(
                {
                    "access_token": str(access_token),
                    "refresh_token": str(refresh_token),
                },
                status=201
            )
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
