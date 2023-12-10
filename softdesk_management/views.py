from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from json import JSONDecodeError
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from softdesk_management.serializers import (
    ProjectSerializer,
    ContributorSerializer
)
from softdesk_management.models import Contributor, Project
from softdesk_management.permissions import IsProjectContributor

class ProjectAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProjectContributor]

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
                project = serializer.save()
                Contributor.objects.create(
                    project=project,
                    user=request.user
                )
                return JsonResponse(
                    {
                        "message": "project successfully created",
                        "project ID": project.pk,
                    },
                    status=200
                )
        except JSONDecodeError:
            return JsonResponse(
                {
                    "response": "error",
                    "message": "JSON decoding error"
                },
                status=400)

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        return JsonResponse(
            {
                "project_id": project.pk,
                "project_name": project.name,
            },
            status=200
        )

    def put(self, request):
        pass

    def delete(self, request):
        pass


class ContributorAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            data = JSONParser().parse(request)
            serializer = ContributorSerializer(
                data=data,
                context={
                    "request": request
                }
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse(
                    {
                        "response": "success",
                        "message": "You now contribute to project"
                    },
                    status=200
                )
        except JSONDecodeError:
            return JsonResponse(
                {
                    "response": "error",
                    "message": "JSON decoding error"
                },
                status=400)

