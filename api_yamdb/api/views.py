from api.filters import TitleFilterSet
from api.mixins import ListCreateDestroy
from api.permissions import AdminHut, IsAdmin, IsOwnerOrStaffOrReadOnly
from api.serializers import (CategorySerializer, CommentSerializer,
                             CreateTokenSerializer, GenreSerializer,
                             ReviewSerializer, SignupSerializer,
                             TitleGetSerializer, TitlePostSerializer,
                             UserSerializer)
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


class CategoriesViewSet(ListCreateDestroy):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (AdminHut,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrStaffOrReadOnly,)

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrStaffOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class GenreViewSet(ListCreateDestroy):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminHut,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (AdminHut,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterSet
    search_fields = ('name',)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TitleGetSerializer
        return TitlePostSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False, methods=['GET', 'PATCH'],
        url_path='me', url_name='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


def send_token(username, email, code):
    send_mail(
        'Registration',
        f'''
        Спасибо за регистрацию {username},
        ващ код подтверждения {code}
        ''',
        'Yamdb@mail.org', [email], fail_silently=False
    )


@api_view(['POST'])
def create_token(request):
    serializer = CreateTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    token = RefreshToken.for_user(serializer.validated_data)
    return Response({'access': str(token.access_token)},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    send_token(
        user.username,
        user.email,
        default_token_generator.make_token(user)
    )
    return Response(serializer.data, status=status.HTTP_200_OK)
