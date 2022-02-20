from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView
from rest_framework.response import Response

from .serializers import *


class ServiceListAPIView(ListAPIView):
    serializer_class = ServiceModelSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        q = self.request.GET.get('q')
        if pk:
            return ProductModel.objects.filter(category_id=pk)
        elif q:
            return ProductModel.objects.filter(title__icontains=q)
        else:
            return ProductModel.objects.none()


class CategoryListAPIView(ListAPIView):
    serializer_class = CategoryModelSerializer
    queryset = CategoryModel.objects.all()


class ProductRetrieveAPIView(RetrieveAPIView):
    serializer_class = ServiceModelSerializer
    queryset = ProductModel.objects.all()


class OrderCreateView(CreateAPIView):
    serializer_class = OrderModelSerializer
    queryset = OrderModel.objects.all()


class UserListAPIView(ListAPIView):
    serializer_class = UserModelSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk:
            return TelegramUserModel.objects.filter(tg_id=pk)
        return TelegramUserModel.objects.all()


class OrderListAPIView(ListAPIView):
    serializer_class = OrderModelSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk:
            return OrderModel.objects.filter(user_id=pk)
        return OrderModel.objects.all()


class KorzinCreateView(CreateAPIView):
    serializer_class = KorzinaModelSerializer

    def create(self, request, *args, **kwargs):
        user_id = self.request.POST.get('user_id')
        product = self.request.POST.get('product')
        price = self.request.POST.get('price')
        count = self.request.POST.get('count')
        qs = KorzinaModel.objects.filter(user_id=user_id, product=product, price=price)
        if not qs:
            KorzinaModel.objects.create(user_id=user_id, product=product, price=price, count=count)
        qs.update(user_id=user_id, product=product, price=price, count=count)
        return Response(status=status.HTTP_201_CREATED)


class KorzinListView(ListAPIView):
    serializer_class = KorzinaModelSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk:
            return KorzinaModel.objects.filter(user_id=pk)
        return KorzinaModel.objects.all()


class KorzinaDestroyView(DestroyAPIView):
    serializer_class = KorzinaModelSerializer
    queryset = KorzinaModel.objects.all()


@api_view(['GET'])
def KorzinaDelateAPIView(request, *args, **kwargs):
    user = kwargs.get('user')
    qs = KorzinaModel.objects.filter(user_id=user)
    if qs:
        for i in qs:
            i.delete()
    return Response(status=status.HTTP_200_OK)


class TelegramRegistrationView(CreateAPIView):
    serializer_class = TelegramRegistrationSerializer
    queryset = TelegramUserModel.objects.all()

