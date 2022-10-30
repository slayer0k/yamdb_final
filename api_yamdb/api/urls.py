from api.views import (CategoriesViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitlesViewSet, UserViewSet, create_token,
                       signup)
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('categories', CategoriesViewSet, basename="categories")
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitlesViewSet, basename='titles')
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/auth/token/', create_token, name='create_token'),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/', include(router.urls)),
]
