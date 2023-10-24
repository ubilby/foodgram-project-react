from djoser.views import UserViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Account
from .serializers import AccountSerializer
from backend.permissions import IsAccountOwnerOrAdminOrReadOnly


class AccountVeiwSet(UserViewSet):
    serializer_class = AccountSerializer
    permission_classes = [IsAccountOwnerOrAdminOrReadOnly, ]
    queryset = Account.objects.all()

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
