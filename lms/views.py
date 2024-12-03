from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Lesson, Subscription
from lms.paginations import CustomPagination
from lms.serializers import CourseSerializer, LessonSerializer
from lms.tasks import send_course_update_email
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.updated_at and now() - instance.updated_at < timedelta(hours=4):
            return Response({"detail": "Курс недавно обновлялся"}, status=400)

        instance.updated_at = now()
        instance.save()

        subscribers = instance.subscribers.all()
        for subscriber in subscribers:
            send_course_update_email.delay(instance.id, subscriber.email)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

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


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = request.data.get('course_id')

        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"

        return Response({"message": message})
