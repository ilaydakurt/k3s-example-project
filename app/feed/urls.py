from django.conf.urls import url
from django.urls import path, include


from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings

router = DefaultRouter()
router.register("post", views.PostViewSet)


app_name = "feed"

urlpatterns = [
    path("", include(router.urls))
]

