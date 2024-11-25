from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField
from lms.models import Course, Lesson
from lms.validators import validate_links


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [validate_links]


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, source='lesson_set', read_only=True)
    is_subscribed = SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, obj):
        return obj.lesson_set.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return obj.subscriptions.filter(user=user).exists()
