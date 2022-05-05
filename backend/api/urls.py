from django.contrib import admin
from django.urls import path

from rest_framework import routers
from django.urls import include
from api import views

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
