import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_user_client_api_register(admin_client):
    user_object = {
        "email": "user@example.com",
        "name": "test",
        "password": "test_pass",
    }
    url = reverse('api-user:register_client')
    response = admin_client.post(url, data=user_object)

    assert response.status_code == status.HTTP_201_CREATED


def test_user_chef_api_register(admin_client):
    user_object = {
        "email": "user@example.com",
        "name": "test",
        "password": "test_pass",
    }
    url = reverse('api-user:register_chef')
    response = admin_client.post(url, data=user_object)

    assert response.status_code == status.HTTP_201_CREATED


def test_user_api_list(admin_client):
    url = reverse('api-user:list_user')
    response = admin_client.get(url, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK


def test_user_api_detail(admin_client, user):
    url = reverse('api-user:retrieve_user', args=[user.id])
    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == user.id


def test_user_api_put(admin_client, user):
    url = reverse('api-user:update_user', args=[user.id])
    response = admin_client.put(url, data={
        "email": "new_user@example.com",
        "name": "new_test"
    })
    assert response.status_code == status.HTTP_200_OK


def test_user_api_delete(admin_client, user):
    url = reverse('api-user:delete_user', args=[user.id])
    response = admin_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_user_api_authenticate(admin_client, user):
    user_object = {
        "username": user.username,
        "password": user.password
    }

    url = reverse('api-user:authenticate_user')
    response = admin_client.post(url, data=user_object)
    assert response.status_code == status.HTTP_200_OK


def test_user_api_change_pass(admin_client, user):
    user_object = {
        "old_password": user.password,
        "password": '123456teste'
    }

    url = reverse('api-user:change_password', args=[user.id])
    response = admin_client.post(url, data=user_object)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED