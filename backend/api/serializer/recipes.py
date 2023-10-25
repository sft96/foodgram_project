from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipes.models import (
    Recipe, Tag, Favorite, ShoppingCart, RecipeIngredient,
)
from api.serializer.ingredients import IngredientAmountSerializer
from api.serializer.users import UserListSerializer
from api.serializer.tags import TagSerializer


class RecipeIngredientSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(source='ingredient_id')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = UserListSerializer()
    ingredients = IngredientAmountSerializer(
        source='recipeingredient_set',
        read_only=True, many=True)
    tags = TagSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def in_list(self, obj, model):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return model.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_favorited(self, obj):
        return self.in_list(obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        return self.in_list(obj, ShoppingCart)


class RecipeSerializer(serializers.ModelSerializer):

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )
    author = UserListSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def to_representation(self, instance):
        serializer = RecipeReadSerializer(instance)
        return serializer.data

    def add_ingredients(self, ingredients, recipe):
        relations = [RecipeIngredient(
                     recipe=recipe,
                     ingredient_id=ingredient_data['ingredient_id'],
                     amount=ingredient_data['amount']
                     ) for ingredient_data in ingredients
                     ]
        RecipeIngredient.objects.bulk_create(relations)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        ingredient_names = [ingredient['name'] for ingredient in ingredients]
        if len(set(ingredient_names)) != len(ingredient_names):
            raise ValidationError('»нгредиенты должны быть уникальными.')
        for ingredient in ingredients:
            if ingredient['amount'] <= 0:
                raise ValidationError(' оличество ингредиентов должно быть '
                                      'больше нул€.')

        tag_names = [tag['name'] for tag in tags]
        if len(set(tag_names)) != len(tag_names):
            raise ValidationError('“еги должны быть уникальными.')

        recipe = super().create(validated_data)
        recipe.tags.set(tags)
        self.add_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.ingredients.clear()
        instance.tags.clear()
        self.add_ingredients(ingredients, instance)
        instance.tags.set(tags)
        return super().update(instance, validated_data)


class ShortRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(source='recipe.name')
    image = serializers.SerializerMethodField()
    cooking_time = serializers.IntegerField(source='recipe.cooking_time')

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)
        read_only_fields = ('id', 'name', 'image', 'cooking_time',)

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.recipe.image:
            url = obj.recipe.image.url
            return request.build_absolute_uri(url)
