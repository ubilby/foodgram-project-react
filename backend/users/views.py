from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Account
from .serializers import AccountSerializer, SubscribesSerializer
from .pagination import AccountLimitPagination
from backend.permissions import IsOwnerAdminOrReadOnly


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
        subscriptions = request.user.subscriptions.all()
        page = pagination.paginate_queryset(subscriptions, request)
        if page is not None:
            serializer = SubscribesSerializer(page, many=True)
            return pagination.get_paginated_response(serializer.data)

        serializer = SubscribesSerializer(subscriptions, many=True)
        return Response(serializer.data)

    @action(
        methods=['post', 'delete'],
        detail=False, permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, pk):
        user = request.user
        author = get_object_or_404(Account, id=pk)

        if request.method == 'POST':
            if user.subscriptions.filter(id=pk).exists() or user.pk == pk:
                return Response({'error': 'Uncorrect action!'}, status=status.HTTP_400_BAD_REQUEST)
            user.subscriptions.add(author)
            serializer = SubscribesSerializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            if user.subscriptions.filter(id=pk).exists():
                user.subscriptions.remove(author)
                return Response({'message': 'Unsubscribed successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'You are not subscribed to this user.'}, status=status.HTTP_400_BAD_REQUEST)
