from datetime import timedelta
from django.utils import timezone
from oauth2_provider.models import AccessToken, Application
from rest_framework.test import APIClient
from recipe.models import Recipe, Ingredient
from user.models import User
import pytest


@pytest.fixture
def admin_client(admin_user, application_client):
    access_token = AccessToken.objects.create(
        user=admin_user,
        scope="read write",
        expires=timezone.now() + timedelta(seconds=300),
        token="secret-access-token-key",
        application=application_client
    )

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token.token)
    client.force_authenticate(user=admin_user)

    return client


@pytest.fixture
def application_client(admin_user):
    return Application.objects.create(
        name="Test Application",
        redirect_uris="http://localhost http://example.com http://example.org",
        user=admin_user,
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
    )


@pytest.fixture
def user():
    user = User()
    user.name = 'test_user'
    user.email = "user@example.com"
    user.password = "test_pass"
    user.save()
    return user


@pytest.fixture
def ingredient():
    ingredient = Ingredient()
    ingredient.name = 'test_name_ingredient'
    ingredient.amount = "test_amount_ingredient"
    ingredient.save()
    return ingredient


@pytest.fixture
def recipe():
    ingredient = Ingredient()
    ingredient.name = "test_name_ingredient"
    ingredient.amount = "test_amount_ingredient"
    ingredient.save()

    user = User()
    user.name = 'test_name'
    user.email = "user@example.com"
    user.password = "test_pass"
    user.save()

    recipe = Recipe()
    recipe.recipe_name = 'test_recipe'
    recipe.preparation_mode = 'test_preparation_mode'
    recipe.chef = user
    recipe.save()
    recipe.ingredient.add(ingredient)
    return recipe