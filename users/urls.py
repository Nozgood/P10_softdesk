from django.urls import path
from users import views

app_name = "users"

urlpatterns = [
    path('signup/', views.SignUpAPIView.as_view(), name='signup'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
]
