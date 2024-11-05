from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet, TextViewSet, LabelViewSet

router = DefaultRouter()
router.register(r'datasets', DatasetViewSet)
router.register(r'texts', TextViewSet)
router.register(r'labels', LabelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
