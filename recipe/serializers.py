from rest_framework import serializers
from .models import Ingredient, Recipe, User


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'type_user'
        ]


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(many=True)
    chef = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Recipe
        fields = (
            'id',
            'chef',
            'recipe_name',
            'ingredient',
            'preparation_mode',

        )
        read_only_fields = [
            'id',
        ]

    def add_ingredients(self, ingredients, recipe):
        for row in ingredients:
            ingredients_objects = Ingredient.objects.create(**row)
            recipe.ingredient.add(ingredients_objects)

    def create(self, validated_data):
        ingredient_objects = validated_data['ingredient']
        del validated_data['ingredient']
        recipe = Recipe.objects.create(**validated_data)
        self.add_ingredients(ingredient_objects, recipe)
        return recipe


class RecipeListRetrieveSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(many=True)
    chef = UserSerializer(many=False)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'chef',
            'recipe_name',
            'ingredient',
            'preparation_mode',
        )


class RecipeUpdateSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'recipe_name',
            'ingredient',
            'preparation_mode'
        )
        read_only_fields = [
            'id'
        ]

    def add_ingredients(self, ingredients, recipe):
        for row in ingredients:
            ingredients_objects = Ingredient.objects.create(**row)
            recipe.ingredient.add(ingredients_objects)

    def update(self, instance, validated_data):
        if "ingredient" in validated_data:
            ingredient_objects = validated_data['ingredient']
            del validated_data['ingredient']

            if ingredient_objects:
                for row in instance.ingredient.values():
                    Ingredient.objects.filter(id=row['id']).delete()

            Recipe.objects.filter(id=instance.id).update(**validated_data)
            recipe = Recipe.objects.get(id=instance.id)
            self.add_ingredients(ingredient_objects, recipe)
            return recipe
        else:
            Recipe.objects.filter(id=instance.id).update(**validated_data)
            recipe = Recipe.objects.get(id=instance.id)
        return recipe

    def validate(self, attrs):
        chef_recipe_id = self.instance.chef.id
        user_token = self.context['request'].user
        if not user_token.is_superuser:
            if user_token.type_user == 'C' and user_token.id == chef_recipe_id:
                pass
            else:
                raise serializers.ValidationError(
                    {'validation': 'You are not allowed to update.'})
        return super().validate(attrs)


