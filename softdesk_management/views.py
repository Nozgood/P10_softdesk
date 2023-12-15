from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from json import JSONDecodeError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from softdesk_management import serializers
from softdesk_management.models import Contributor, Project
from softdesk_management.permissions import (
    IsProjectContributor,
    IsProjectAuthor,
)

class ProjectAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsProjectContributor,
        IsProjectAuthor
    ]

    @staticmethod
    def post(request):
        try:
            data = JSONParser().parse(request)
            serializer = serializers.ProjectSerializer(
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

    @staticmethod
    def get(request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        return JsonResponse(
            {
                "project_id": project.pk,
                "project_name": project.name,
                "description": project.description,
                "project_type": project.type,
                "created_at": project.created_at,
            },
            status=200
        )

    @staticmethod
    def put(request, project_id):
        try:
            project = get_object_or_404(Project, pk=project_id)
            data = JSONParser().parse(request)
            serializer = serializers.ProjectSerializer(project, data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse(
                    {
                        "response": "success",
                        "message": "project successfully updated"
                    },
                    status=200
                )
        except JSONDecodeError:
            return JsonResponse(
                {
                    "response": "error",
                    "message": "JSON decoding error"
                },
                status=400
            )

    def delete(self, request, project_id):
        try:
            project = get_object_or_404(Project, pk=project_id)
            project.delete()
            return JsonResponse(
                {
                    "response": "success",
                    "message": "project successfully deleted",
                },
                status=200)

        except JSONDecodeError:
            return JsonResponse(
                {
                    "response": "error",
                    "message": "JSON decoding error"
                },
                status=400
            )


class ContributorAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            data = JSONParser().parse(request)
            serializer = serializers.ContributorSerializer(
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

class IssueAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            data = JSONParser().parse(request)
            serializer = serializers.IssueSerializer(
                data=data,
                context={
                    "request": request
                }
            )
            if serializer.is_valid(raise_exception=True):
                issue = serializer.save()
                return JsonResponse(
                    {
                        "message": "success",
                        "issue_id": issue.id
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
