from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users import urls as user_urls

router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('api/users/', include(user_urls)),
]
