from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComputerViewSet, PartViewSet, GameViewSet, CartViewSet, ShopViewSet, register_user, login_user

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'computers', ComputerViewSet)
router.register(r'parts', PartViewSet)
router.register(r'games', GameViewSet)
router.register(r'carts', CartViewSet)
router.register(r'shops', ShopViewSet)

urlpatterns = [
    # Include the router URLs
    path('api/', include(router.urls)),

    # Custom endpoints for user registration and login
    path('api/register/', register_user, name='register'),
    path('api/login/', login_user, name='login'),
]
