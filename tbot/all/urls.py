from django.urls import path

from .views import *

urlpatterns = [
    path('user/register/', TelegramRegistrationView.as_view()),
    path('category/', CategoryListAPIView.as_view()),
    path('prod/', ServiceListAPIView.as_view()),
    path('category/<int:pk>/', ServiceListAPIView.as_view()),
    path('products/<int:pk>/', ProductRetrieveAPIView.as_view()),
    path('order/', OrderCreateView.as_view()),
    path('user/<int:pk>/', UserListAPIView.as_view()),
    path('user/', UserListAPIView.as_view()),
    path('order/<int:pk>/', OrderListAPIView.as_view()),
    path('korzina/list/<int:pk>/', KorzinListView.as_view()),
    path('korzina/delete/<int:pk>/', KorzinaDestroyView.as_view()),
    path('korzina/clear/<int:user>/', KorzinaDelateAPIView),
    path('korzina/create/', KorzinCreateView.as_view()),
]
