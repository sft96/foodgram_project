from django.http import HttpResponse

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from recipes.models import Recipe, ShoppingCart
from api.serializer.cart import ShoppingCartSerializer
from api.view.recipes import AddDeleteView


class ShoppingCartView(AddDeleteView):
    add_model = Recipe
    delete_model = ShoppingCart
    add_serializer = ShoppingCartSerializer

    def post(self, request, pk):
        return self.add_recipe(request, pk)

    def delete(self, request, pk):
        return self.delete_pecipe(request, pk)


class DownloadShoppingCart(ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        recipes_ingredients = Recipe.objects.filter(
            in_carts__user=self.request.user).distinct()
        shopcart = {}

        for recipe in recipes_ingredients:
            recipe_ingredients = recipe.ingredients.all()
            for ingredient in recipe_ingredients:
                if ingredient.name not in shopcart:
                    shopcart[ingredient.name] = {
                        'amount': 0,
                        'measurement_unit': ingredient.measurement_unit
                    }
                amount = ingredient.recipeingredient_set.filter(
                    recipe=recipe).first().amount
                shopcart[ingredient.name]['amount'] += amount

        shoppincart = ''
        for item in shopcart:
            shoppincart += f'{item}:\n'
            shoppincart += (f'\t{shopcart[item]["amount"]} '
                            f'{shopcart[item]["measurement_unit"]}\n')

        filename = '{}_shopping_cart.txt'.format(self.request.user)
        response = HttpResponse(
            shoppincart, content_type='text/plain; charset=utf-8'
        )
        response['Content-Disposition'] = (
            'attachment; filename={}'.format(filename)
        )
        return response
