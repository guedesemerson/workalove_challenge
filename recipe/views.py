from rest_framework.generics import (ListAPIView,
                                     GenericAPIView,
                                     RetrieveAPIView,
                                     DestroyAPIView,
                                     UpdateAPIView)
from .serializers import (RecipeCreateSerializer,
                          RecipeUpdateSerializer,
                          RecipeListRetrieveSerializer,
                          )
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend
from .models import Recipe


class RegisterRecipeView(GenericAPIView):
    serializer_class = RecipeCreateSerializer

    def post(self, request):
        serializer = RecipeCreateSerializer(data=request.data, context={'request': request})
        user_token = self.request.parser_context['request'].user
        if user_token.type_user == 'C' or user_token.is_superuser:
            pass
        else:
            raise serializers.ValidationError(
                {'validation': 'You are Client. Please log in as a chef.'})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListRecipeView(ListAPIView):

    serializer_class = RecipeListRetrieveSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]

    #filtering by chef and recipe_name
    filterset_fields = ['chef', 'recipe_name']

    def get_queryset(self):
        user_token = self.request.parser_context['request'].user
        if user_token.type_user == 'P' or user_token.is_superuser:
            pass
        else:
            raise serializers.ValidationError(
                {'validation': 'You are chef. Please enter as a client.'})
        return Recipe.objects.all()


class RetrieveRecipeView(RetrieveAPIView):

    serializer_class = RecipeListRetrieveSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        user_token = self.request.parser_context['request'].user
        if user_token.type_user == 'P' or user_token.is_superuser:
            pass
        else:
            raise serializers.ValidationError(
                {'validation': 'You are chef. Please enter as a client.'})

        return Recipe.objects.filter(id=self.kwargs['id'])


class DeleteRecipeView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        queryset = Recipe.objects.filter(id=self.kwargs['id'])
        return queryset

    def perform_destroy(self, instance):
        user_token = self.request.parser_context['request'].user
        if not user_token.is_superuser:
            if user_token.type_user == 'C' and user_token.id == instance.chef.id:
                pass
            else:
                raise serializers.ValidationError(
                    {'validation': 'Not allowed to delete this recipe.'}
                )

        instance.delete()


class UpdateRecipeView(UpdateAPIView):
    serializer_class = RecipeUpdateSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Recipe.objects.filter(id=self.kwargs['id'])
        return queryset

    def perform_update(self, serializer):
        serializer.save()
