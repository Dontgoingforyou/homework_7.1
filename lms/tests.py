from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from .models import Course, Lesson, Subscription


class CourseTestCase(APITestCase):
    def setUp(self):
        """ Создание пользователя, курса, урока и добавление урока в курс """

        self.user = User.objects.create(email="user@example.com")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Test Course")
        self.lesson = Lesson.objects.create(title='Test Lesson')
        self.course.lesson_set.add(self.lesson)

    def test_create_course(self):
        """ Тестирование добавления курса """

        url = reverse('lms:course-list')
        data = {"title": "New Lesson"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_list_courses(self):
        """ Тестирование отображения курсов """

        url = reverse('lms:course-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_retrieve_course(self):
        """ Тестирование отображения курса """

        url = reverse('lms:course-detail', args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.course.title)

    def test_update_course(self):
        """ Тестирование редактирования курса """

        url = reverse('lms:course-detail', args=(self.course.pk,))
        data = {"title": "Updated Course"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Updated Course")

    def test_delete_course(self):
        """ Тестирование удаления курса """

        url = reverse('lms:course-detail', args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)


class LessonTestsCase(APITestCase):
    def setUp(self):
        """ Создание пользователя, курса, урока и добавление урока в курс """

        self.user = User.objects.create(email="user@example.com")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Test Course")
        self.lesson = Lesson.objects.create(title='Test Lesson')
        self.course.lesson_set.add(self.lesson)

    def test_create_lesson(self):
        """ Тестирование создания урока """

        url = reverse('lms:lesson-list-create')
        data = {"title": "New Lesson"}
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get("title"), "New Lesson")

    def test_list_lessons(self):
        """ Тестирование отображения уроков """

        url = reverse('lms:lesson-list-create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_retrieve_lesson(self):
        """ Тестирование отображения урока """

        url = reverse('lms:lesson-detail', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_update_lesson(self):
        """ Тестирование редактирования урока """

        url = reverse('lms:lesson-detail', args=(self.lesson.pk,))
        data = {"title": "Updated Lesson"}
        response = self.client.put(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Updated Lesson")

    def test_delete_lesson(self):
        """ Тестирование удаления урока """

        url = reverse('lms:lesson-detail', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscriptionViewTests(APITestCase):
    def setUp(self):
        """ Создание пользователя, курса, урока и добавление урока в курс """

        self.user = User.objects.create(email="user@example.com")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Test Course")
        self.lesson = Lesson.objects.create(title='Test Lesson')
        self.course.lesson_set.add(self.lesson)

    def test_subscribe_to_course(self):
        """ Тестирование подписки """

        url = reverse('lms:subscribe')
        data = {"course_id": self.course.id}
        response = self.client.post(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('message'), "Подписка добавлена")
        self.assertEqual(Subscription.objects.all().count(), 1)

    def test_unsubscribe_from_course(self):
        """ Тестирование отписки """

        url = reverse('lms:subscribe')
        data = {"course_id": self.course.id}
        # Сначала подписываемся
        self.client.post(url, data)
        # Затем отписываемся
        response = self.client.post(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('message'), "Подписка удалена")
        self.assertEqual(Subscription.objects.all().count(), 0)

    def test_invalid_course_id(self):
        """ Тестирование подписки для невалидного курса """

        url = reverse('lms:subscribe')
        data = {"course_id": 9999}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
