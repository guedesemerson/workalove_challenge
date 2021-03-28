from rest_framework.generics import (ListAPIView,
                                     GenericAPIView,
                                     RetrieveAPIView,
                                     DestroyAPIView,
                                     UpdateAPIView)
from .serializers import (ClientSignupSerializer,
                          ChefSignupSerializer,
                          UserAuthenticateSerializer,
                          UserListSerializer,
                          UserRetrieveSerializer,
                          UserUpdateSerializer,
                          ResetUserPasswordSerializer)
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import serializers
from .models import User
import jwt


class RegisterClienteView(GenericAPIView):
    serializer_class = ClientSignupSerializer

    def post(self, request):
        serializer = ClientSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterChefView(GenericAPIView):
    serializer_class = ChefSignupSerializer

    def post(self, request):
        serializer = ChefSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthenticateUserView(GenericAPIView):
    serializer_class = UserAuthenticateSerializer

    def post(self, request):
        data = request.data
        email = data.get('email', '')
        password = data.get('password', '')

        try:
            object_pass = User.objects.get(email=email)
        except:
            return Response({'detail': 'Invalid credentials'})

        username = object_pass.username
        user = authenticate(username=username, password=password)

        if not user:
            user = User.objects.filter(username=username, password=password)

        if user:
            auth_token = jwt.encode(
                {'username': username}, str(settings.JWT_SECRET_KEY))

            data = {'email': email, 'token': auth_token}

            return Response(data, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ListUserProfileView(ListAPIView):

    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.all()


class RetrieveUserProfileView(RetrieveAPIView):

    serializer_class = UserRetrieveSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        user_token = self.request.parser_context['request'].user
        if user_token.id == self.kwargs['id'] or user_token.is_superuser:
            pass
        else:
            raise serializers.ValidationError(
                {'validation': 'You are not allowed to search this profile.'})

        return User.objects.filter(id=self.kwargs['id'])


class DeleteUserProfileView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        queryset = User.objects.filter(id=self.kwargs['id'])
        return queryset

    def perform_destroy(self, instance):
        user_token = self.request.parser_context['request'].user
        if user_token == instance or user_token.is_superuser:
            pass
        else:
            raise serializers.ValidationError(
                {'validation': 'You are not allowed to delete another user profile.'})

        instance.delete()


class UpdateUserProfile(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        queryset = User.objects.filter(id=self.kwargs['id'])
        return queryset

    def perform_update(self, serializer):
        serializer.save()


class ChangePassUserView(UpdateAPIView):
    serializer_class = ResetUserPasswordSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        queryset = User.objects.filter(id=self.kwargs['id'])
        return queryset

    def perform_update(self, serializer):
        serializer.save()