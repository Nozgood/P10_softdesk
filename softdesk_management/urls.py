from django.urls import path
from softdesk_management import views

app_name = "softdesk"

urlpatterns = [
    path(
        'project/create/',
        views.ProjectCreateView.as_view(),
        name='create_project'
    ),
    path(
        'project/get/<int:pk>',
        views.ProjectGetView.as_view(),
        name='create_project'
    ),
    path(
        'project/update/<int:pk>',
        views.ProjectUpdateView.as_view(),
        name='update_project'
    ),
    path(
        'project/delete/<int:pk>',
        views.ProjectDeleteView.as_view(),
        name='delete_project'
    ),
    path(
        'projects',
        views.ProjectListView.as_view(),
        name='list_projects'
    ),
    path(
        'project/contribute/',
        views.ContributorCreateView.as_view(),
        name="contribute"
    )
]
