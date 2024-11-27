from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User, Payment
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal


class UserViewSetTestCase(APITestCase):
    def setUp(self):
        """ Создание пользователя и установка JWT-токена для авторизации """

        self.user = User.objects.create(email='user@example.com', password='password')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_user_list(self):
        """ Тестирование отображения пользователей """

        url = reverse('users:user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_user_search(self):
        """ Тестирование поиска пользователей по email """

        url = reverse('users:user-list')
        data = {'search': 'user@example.com'}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_user_ordering(self):
        """ Тестирование сортировки пользователей """

        url = reverse('users:user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserCreateAPIViewTests(APITestCase):
    def test_create_user(self):
        """ Тестирование создания пользователя """

        url = reverse('users:register')
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword',
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)


class UserProfileViewTests(APITestCase):
    def setUp(self):
        """ Создание пользователя и установка JWT-токена для авторизации """

        self.user = User.objects.create(email='user@example.com', password='password')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_get_user_profile(self):
        """ Тестирование получения детальной информации о пользователе """

        url = reverse('users:user-profile', args=(self.user.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_update_user_profile(self):
        """ Тестирование редактирования детальной информации о пользователе """

        url = reverse('users:user-profile', args=(self.user.pk,))
        data = {'first_name': 'NewFirstName'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'NewFirstName')


class PaymentTestCase(APITestCase):
    def setUp(self):
        """ Создание пользователя, установка JWT-токена для авторизации и создание платежа """

        self.user = User.objects.create(email='user@example.com', password='password')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.payment = Payment.objects.create(amount=50.0, user=self.user, payment_method='cash')

    def test_create_payment(self):
        """ Тестирование создания платежа """

        url = reverse('users:payment-list-create')
        data = {'amount': 100.0, 'user': self.user.pk, 'payment_method': 'transfer'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 2)

    def test_list_payments(self):
        """ Тестирование отображения платежей """

        url = reverse('users:payment-list-create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_retrieve_payment(self):
        """ Тестирование отображения данных платежа """

        url = reverse('users:payment-detail', args=(self.payment.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(data.get('amount')), Decimal('50.00'))

    def test_update_payment(self):
        """ Тестирование редактирования платежа """

        url = reverse('users:payment-detail', args=(self.payment.pk,))
        data = {'amount': 200.0}
        response = self.client.patch(url, data)
        self.payment.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.payment.amount, 200.0)

    def test_delete_payment(self):
        """ Тестирование удаления платежа """

        url = reverse('users:payment-detail', args=(self.payment.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Payment.objects.all().count(), 0)
