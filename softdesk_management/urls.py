from django.urls import path
from softdesk_management.views import ProjectAPIView

app_name = "softdesk"

urlpatterns = [
    path('project/create/', ProjectAPIView.as_view(), name='create_project'),
    path('project/get/', ProjectAPIView.as_view(), name='create_project'),
    path('project/update/', ProjectAPIView.as_view(), name='create_project'),
    path('project/delete/', ProjectAPIView.as_view(), name='create_project')
]
