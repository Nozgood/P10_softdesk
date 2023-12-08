from django.urls import path
from softdesk_management.views import ProjectAPIView

app_name = "softdesk"

urlpatterns = [
    path('project/create/', ProjectAPIView.as_view(), name='create_project'),
    path(
        'project/get/<int:id>',
        ProjectAPIView.as_view(),
        name='create_project'
    ),
    path(
        'project/update/<int:id>',
        ProjectAPIView.as_view(),
        name='update_project'
    ),
    path(
        'project/delete/<int:id>',
        ProjectAPIView.as_view(),
        name='delete_project'
    )
]
