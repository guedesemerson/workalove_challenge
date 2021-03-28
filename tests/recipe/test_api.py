import pytest
from django.urls import reverse
from rest_framework import status


pytestmark = pytest.mark.django_db


def test_recipe_list(admin_client):
    url = reverse('api-recipe:list_recipe')
    response = admin_client.get(url, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK


def test_recipe_api_detail(admin_client, recipe):
    url = reverse('api-recipe:retrieve_recipe', args=[recipe.id])
    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == recipe.id


def test_recipe_api_update(admin_client, recipe):
    url = reverse('api-recipe:update_recipe', args=[recipe.id])
    response = admin_client.patch(url, data={'recipe_name': 'new_name'})
    assert response.status_code == status.HTTP_200_OK


def test_recipe_api_delete(admin_client, recipe):
    url = reverse('api-recipe:delete_recipe', args=[recipe.id])
    response = admin_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT