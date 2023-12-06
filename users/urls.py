from django.urls import path
from users import views
from rest_framework_simplejwt import views as jwt_views

app_name = "users"

urlpatterns = [
    path('signup/', views.SignUpAPIView.as_view(), name='signup'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('', views.UserAPIView.as_view(), name='get_user'),
    path('update/', views.UserAPIView.as_view(), name='update_user'),
    path('delete/', views.UserAPIView.as_view(), name='delete_user'),
]
