from django.shortcuts import get_object_or_404

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from .paginations import CustomPagination
from .permissions import AdminAuthorPermission
from .user_serializers import (
    UserCreateSerializer,
    UserChangePasswordSerializer,
    UserSerializer,
    SubscriptionCreateSerializer,
    SubscriptionSerializer
)

from users.models import User, Subscription


class UsersViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """
    Пользовательский вьюсет для создания, изменения,
    выдачи объекта или списка объектов.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny, )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        else:
            return UserSerializer

    @action(
        methods=['GET', 'PATCH', ],
        detail=False,
        permission_classes=(AdminAuthorPermission, ),
        url_path='me',)
    def get_current_user_info(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST', ],
            detail=False,
            permission_classes=(IsAuthenticated, ),
            url_path='set_password', )
    def set_password(self, request):
        serializer = UserChangePasswordSerializer(
            request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST', 'DELETE', ],
            detail=True,
            permission_classes=(IsAuthenticated,),
            url_path='subscribe', )
    def get_subscribe(self, request, pk):
        author = get_object_or_404(User, id=pk)
        if request.method == 'POST':
            serializer = SubscriptionCreateSerializer(
                data={'user': self.request.user.id, 'author': pk})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=self.request.user, author=author)
            show_content_serializer = SubscriptionSerializer(
                author, context={'request': request})
            return Response(show_content_serializer.data,
                            status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            get_object_or_404(Subscription, user=request.user,
                              author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET', ],
            detail=False,
            permission_classes=(IsAuthenticated, ),
            pagination_class=CustomPagination,
            url_path='subscriptions',)
    def get_subscriptions(self, request):
        queryset = User.objects.filter(author__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
