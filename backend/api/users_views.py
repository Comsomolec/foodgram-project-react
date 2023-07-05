from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .users_serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserChangePasswordSerializer,
    SubscriptionSerializer,
    SubscriptionCreateSerializer
)
from .paginations import CustomPagination
from .permissions import CurrentUser
from core.mixins import CreateListRetrieveViewSet
from users.models import User, Subscription


class UsersViewSet(CreateListRetrieveViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        else:
            return UserSerializer

    @action(
            detail=False,
            permission_classes=[CurrentUser],
            url_path='me',
            url_name='me',
    )
    def me(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
            detail=False,
            methods=['POST'],
            permission_classes=[CurrentUser],
            url_path = 'set_password',
            url_name = 'set_password',
    )
    def set_password(self, request):
        serializer = UserChangePasswordSerializer(
            request.user, data=request.data
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(
            detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=[IsAuthenticated],
            url_path = 'subscribe',
            url_name = 'subscribe',
    )
    def subscribe(self, request, pk):
        user = self.request.user
        author = get_object_or_404(User, id=pk)
        if request.method == 'POST':
            serializer = SubscriptionCreateSerializer(
                data={'user': user.id, 'author': pk}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user, author=author)
            content_serializer = SubscriptionSerializer(
                author, context={'request': request}
            )
            return Response(
                content_serializer.data, status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            get_object_or_404(Subscription, user=user,
                              author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            permission_classes=[IsAuthenticated],
            pagination_class=CustomPagination,
            url_path = 'subscriptions',
            url_name = 'subscriptions',
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(author__user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscriptionSerializer(
            page, many=True, context={'request': request}
        )
            return self.get_paginated_response(serializer.data)
        serializer = SubscriptionSerializer(
            queryset, many=True, context={'request': request}
        )
        return Response(serializer.data)
