from rest_framework import viewsets, status
from rest_framework.response import Response
from posts.models import Post, Comment, Follow, Group, User
from .serializers import (GroupSerializer,
                          FollowSerializer,
                          PostSerializer,
                          CommentSerializer)
from .permissions import AuthorOrReadOnly
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def create(self, request, *args, **kwargs):
        following_username = request.data.get('following')
        if not following_username:
            return Response({'error': 'Поле "following" обязательно.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if following_username == request.user.username:
            return Response({'error': 'Нельзя подписаться на самого себя.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            following_user = User.objects.get(username=following_username)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(user=request.user, following=following_user)\
                 .exists():
            return Response({'error': 'Вы уже подписаны на этого \
пользователя.'}, status=status.HTTP_400_BAD_REQUEST)
        follow = Follow(user=request.user, following=following_user)
        follow.save()
        serializer = self.get_serializer(follow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

    def create(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        data = request.data.copy()
        data['post'] = post_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        self.object = self.get_object()
        if self.object.post_id != post_id:
            return Response({'detail': 'Неправильно указан id поста.'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(self.object,
                                         data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
