from django.urls import include, path
from rest_framework import routers
from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'follow', FollowViewSet, basename='follow')
router.register(r'groups', GroupViewSet, basename='groups')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/posts/<int:post_id>/comments/', CommentViewSet.as_view(
        {'get': 'list',
         'post': 'create'}
    ), name='post-comments'),
    path('v1/posts/<int:post_id>/comments/<int:pk>/', CommentViewSet.as_view(
        {'get': 'retrieve',
         'put': 'update',
         'patch': 'partial_update',
         'delete': 'destroy'}
    ), name='comment-detail'),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
