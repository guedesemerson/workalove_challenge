from django.urls import path
from .views import (RegisterClienteView,
                    AuthenticateUserView,
                    ListUserProfileView,
                    RetrieveUserProfileView,
                    DeleteUserProfileView,
                    UpdateUserProfile,
                    ChangePassUserView,
                    RegisterChefView)

app_name = "api-user"

urlpatterns = [
    path('register_client', RegisterClienteView.as_view(), name='register_client'),
    path('register_chef', RegisterChefView.as_view(), name='register_chef'),
    path('authenticate_user', AuthenticateUserView.as_view(), name='authenticate_user'),
    path('list_user', ListUserProfileView.as_view(), name='list_user'),
    path('retrieve_user/<int:id>', RetrieveUserProfileView.as_view(), name='retrieve_user'),
    path('delete_user/<int:id>', DeleteUserProfileView.as_view(), name='delete_user'),
    path('update_user/<int:id>', UpdateUserProfile.as_view(), name='update_user'),
    path('change_password/<int:id>', ChangePassUserView.as_view(), name='change_password'),
]