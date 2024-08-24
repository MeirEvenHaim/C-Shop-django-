from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import viewsets from their respective files
from .views.computer_views import ComputerViewSet
from .views.parts_views import PartViewSet
from .views.game_views import GameViewSet
from .views.cart_views import CartViewSet  # Import the CartViewSet
from .views.shop_views import ShopViewSet

# Import API views from their respective files
from .views.user_views import (
    register_user, login_user, list_all_users, user_profile, 
    update_user_profile, delete_user
)
from .views.cart_views import create_cart

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'computers', ComputerViewSet, basename='computer')
router.register(r'parts', PartViewSet, basename='part')
router.register(r'games', GameViewSet, basename='game')
router.register(r'shops', ShopViewSet, basename='shop')
router.register(r'carts', CartViewSet, basename='cart')  # Register the CartViewSet

urlpatterns = [
    # ViewSet URLs
    path('', include(router.urls)),  # Prefix all viewset URLs with 'api/'

    # User management URLs
    path('register/', register_user, name='register_user'),
    path('carts/', create_cart, name='create-cart'),
    path('login/', login_user, name='login_user'),
    path('users/', list_all_users, name='list_all_users'),
    path('profile/', user_profile, name='user_profile'),
    path('profile/update/', update_user_profile, name='update_user_profile'),
    path('users/<int:id>/update/', update_user_profile, name='update_user_profile_by_id'),
    path('users/<int:id>/delete/', delete_user, name='delete_user')]


