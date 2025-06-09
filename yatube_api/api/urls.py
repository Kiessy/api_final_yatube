from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from api.views import GroupViewset, PostViewSet, CommentViewSet, FollowViewSet

router_v1 = DefaultRouter()


router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register('group', GroupViewset, basename='groups')
router_v1.register('follow', FollowViewSet, basename='follow')
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments'
)


urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt'))
]