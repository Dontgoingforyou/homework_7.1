from django.urls import path
from rest_framework.routers import SimpleRouter

from lms.apps import LmsConfig
from lms.views import CourseViewSet, LessonListCreateAPIView, LessonRetrieveUpdateDestroyAPIView

app_name = LmsConfig.name

router = SimpleRouter()
router.register('', CourseViewSet)

urlpatterns = [
    path('lessons/', LessonListCreateAPIView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view(), name='lesson-detail'),
] + router.urls