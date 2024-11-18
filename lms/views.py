from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsAuthenticated | IsModer | IsOwner]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated | IsModer | IsOwner]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAuthenticated | IsModer | IsOwner]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated | IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated | IsOwner]
        elif self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated | IsModer | IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated | IsModer | IsOwner]
        elif self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [IsAuthenticated | IsModer | IsOwner]
        elif self.request.method == 'DELETE':
            self.permission_classes = [IsAuthenticated | IsOwner]
        return super().get_permissions()
