from django.conf import settings
from django.conf.urls.static import static
"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *
from django.contrib.auth import views as auth_views


router = DefaultRouter()
router.register(r'games', VideoGameViewSet, basename='games')  # Pas besoin d'auth pour accéder aux produits
router.register(r'orders', OrderViewSet, basename='orders')  # Nécessite authentification

urlpatterns = [
    path('api/', include(router.urls)),
    path('', trending_games, name='index'),  # Page d'accueil

    # Auth routes
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Cart URLs (non via le router)
    path('api/cart/', CartView.as_view(), name='cart'),
    path('api/cart/items/', CartItemView.as_view(), name='cart_items'),
    path('product/<int:id>/', product_detail, name='product_detail'),
    path('shop/', shop, name='shop'),  # Page de la boutique avec recherche
    path('login/', user_login, name='login'),  # Route pour la page de connexion
    # Page de détail du produit
    path('register/', register, name='register'),  # Route pour l'inscription

    path('auth/', auth_view, name='auth'),  # Route pour la page de connexion et d'inscription

    # Autres routes
    path('logout/', auth_views.LogoutView.as_view(next_page='auth'), name='logout'),

]
# Ajoute cette ligne pour servir les fichiers médias durant le développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
