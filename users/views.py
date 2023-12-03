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
from rest_framework.permissions import IsAuthenticated


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

class GetUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        user = get_object_or_404(User, id=request.user.id)
        return JsonResponse(
            {
                "email": user.email,
                "username": user.username,
                "password": user.password,
                "age": user.age,
                "can_be_contacted": user.can_be_contacted,
                "data_can_be_shared": user.data_can_be_shared
            },
            status=200
        )

class DeleteUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def delete(request):
        user_to_delete = User.objects.get(id=request.user.id)
        user_to_delete.delete()
        return JsonResponse(
            {
                "response": "success",
                "message": "user successfully deleted",
            },
            status=201)


class UpdateUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            user = get_object_or_404(User, id=request.user.id)
            data = JSONParser().parse(request)
            serializer = UserSerializer(user, data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse(
                    {
                        "response": "success",
                        "message": "user successfully updated"
                    },
                    status=201
                )
        except JSONDecodeError:
            return JsonResponse(
                {
                    "response": "error",
                    "message": "JSON decoding error"
                },
                status=400
            )
