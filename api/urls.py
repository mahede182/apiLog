from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet, test_logging

router = DefaultRouter()
router.register(r'notes', NoteViewSet)

urlpatterns = [
    path('test-logging/', test_logging, name='test-logging'),
    path('', include(router.urls)),
] 