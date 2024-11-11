from django.urls import path
from rest_framework.routers import SimpleRouter
from users.apps import UsersConfig
from users.views import UserViewSet, UserListCreateAPIView, UserRetrieveUpdateDestroyAPIView

app_name = UsersConfig.name

router = SimpleRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('profile/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('profile/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),
] + router.urls