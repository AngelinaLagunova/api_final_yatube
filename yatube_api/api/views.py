from rest_framework import viewsets, status
from rest_framework.response import Response
# from rest_framework.pagination import PageNumberPagination
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
    filter_backends = (filters.SearchFilter)
    search_fields = ('search',)

    def create(self, request, *args, **kwargs):
        following = request.data.get('following')
        try:
            following_user = User.objects.get(username=following)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден.'}, status=status.HTTP_404_NOT_FOUND)

        if Follow.objects.filter(user=request.user, following=following_user).exists():
            return Response({'error': 'Вы уже подписаны на этого пользователя.'}, status=status.HTTP_400_BAD_REQUEST)

        follow = Follow(user=request.user, following=following_user)
        follow.save()
        return Response({'message': 'Вы успешно подписались на пользователя.'}, status=status.HTTP_201_CREATED)


class GroupViewSet(viewsets.ModelViewSet):
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
        request.data['post'] = post_id
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

