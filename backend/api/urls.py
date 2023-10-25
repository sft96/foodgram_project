from django.urls import include, path
from rest_framework.routers import DefaultRouter
from djoser.views import UserViewSet
from .users_password import set_password
from .view.subscriptions import (
    SubscribeView,
    SubscriptionView
)
from .view.tags import TagViewSet
from .view.ingredients import IngredientViewSet
from .view.recipes import RecipeViewSet
from .view.cart import DownloadShoppingCart
from .view.favorite import FavoriteView
from .view.cart import ShoppingCartView

router = DefaultRouter()

router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

djoser_urlpatterns = [
    path('me/', UserViewSet.as_view({'get': 'me'}), name='me'),
    path(
        '', UserViewSet.as_view({'post': 'create', 'get': 'list'}),
        name='user_create'
    ),
    path(
        '<int:id>/', UserViewSet.as_view({"get": "retrieve"}), name='user_pk'
    ),
]

user_paths = [
    path('users/subscriptions/', SubscriptionView.as_view()),
    path('users/<int:pk>/subscribe/', SubscribeView.as_view()),
]

recipe_paths = [
    path('recipes/<int:pk>/favorite/', FavoriteView.as_view()),
    path('recipes/download_shopping_cart/', DownloadShoppingCart.as_view()),
    path('recipes/<int:pk>/shopping_cart/', ShoppingCartView.as_view()),
]

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('users/set_password/',
         set_password,
         name='set_password'),
    path('users/', include(djoser_urlpatterns)),
    path('users/', include(user_paths)),
    path('recipe/', include(recipe_paths)),
]
