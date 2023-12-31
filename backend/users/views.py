from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.permissions import IsOwnerAdminOrReadOnly
from subscribes.models import Subscribe
from subscribes.serializers import SubscribeResponseSerializer

from .models import Account
from .pagination import AccountLimitPagination
from .serializers import AccountSerializer


class AccountVeiwSet(UserViewSet):
    serializer_class = AccountSerializer
    permission_classes = [IsOwnerAdminOrReadOnly, ]
    queryset = Account.objects.all()
    pagination_class = AccountLimitPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if 'pk' in kwargs:
            instance = get_object_or_404(queryset, pk=kwargs['pk'])
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    @action(
        methods=['get'], detail=False,
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        pagination = AccountLimitPagination()
        subscriptions = Subscribe.objects.filter(user=request.user)
        page = pagination.paginate_queryset(subscriptions, request)
        recipes_limit = request.GET.get('recipes_limit')
        serializer = SubscribeResponseSerializer(
            page,
            many=True,
            context={
                'recipes_limit': recipes_limit,
                'user': request.user
            }
        )
        return pagination.get_paginated_response(serializer.data)

    @action(
        methods=['post'],
        detail=False, permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, pk):
        user = request.user
        author = get_object_or_404(Account, id=pk)
        recipes_limit = request.GET.get('recipes_limit')
        serializer = SubscribeResponseSerializer(
            data={
                'user': user.id,
                'author': author.id
            },
            context={
                'recipes_limit': recipes_limit,
                'user': request.user
            }
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, pk):
        user = request.user
        author = get_object_or_404(Account, id=pk)
        subscribe = get_object_or_404(Subscribe, user=user, author=author)
        subscribe.delete()
        return Response(
            {'message': 'Unsubscribed successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )
