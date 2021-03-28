from django.urls import path
from .views import (RegisterRecipeView,
                    ListRecipeView,
                    RetrieveRecipeView,
                    DeleteRecipeView,
                    UpdateRecipeView,
                    )

app_name = "api-recipe"

urlpatterns = [
    path('register_recipe', RegisterRecipeView.as_view(), name='register_recipe'),
    path('list_recipe', ListRecipeView.as_view(), name='list_recipe'),
    path('retrieve_recipe/<int:id>', RetrieveRecipeView.as_view(), name='retrieve_recipe'),
    path('delete_recipe/<int:id>', DeleteRecipeView.as_view(), name='delete_recipe'),
    path('update_recipe/<int:id>', UpdateRecipeView.as_view(), name='update_recipe')
]