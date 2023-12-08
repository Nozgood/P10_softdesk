from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from json import JSONDecodeError
from django.http import JsonResponse
from softdesk_management.serializers import ProjectSerializer

class ProjectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            data = JSONParser().parse(request)
            print(f"data: {data}")
            serializer = ProjectSerializer(
                data=data,
                context={"request": request}
            )
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

    def get(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass