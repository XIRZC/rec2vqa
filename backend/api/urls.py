from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from api import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'recs', views.RECViewSet)
router.register(r'vqas', views.VQAViewSet)
router.register(r'imgs', views.IMGViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^socket/', views.socket, name='socket')
]
