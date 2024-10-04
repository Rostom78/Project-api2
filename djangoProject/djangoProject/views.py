from rest_framework import viewsets, generics, permissions
from .models import *
from .serializers import VideoGameSerializer, CartSerializer, CartItemSerializer, OrderSerializer

from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout


def trending_games(request):
    # Récupérer les 5 derniers jeux vidéo
    trending_games = VideoGame.objects.all()[:5]  # Limite à 5 jeux
    return render(request, 'djangoProject/index.html', {'trending_games': trending_games})

from django.shortcuts import render
from .models import VideoGame

from django.shortcuts import render
from .models import VideoGame

@login_required(login_url='/login/')  # Redirige vers la page de login si non authentifié
def shop(request):
    # Récupérer les filtres depuis les paramètres GET
    search_keyword = request.GET.get('searchKeyword', '')
    selected_category = request.GET.get('category', '')
    max_price = request.GET.get('price', 1000)  # Prix maximal par défaut à 1000 $

    # Commencer par récupérer tous les jeux
    games = VideoGame.objects.all()

    # Filtrer par catégorie si une catégorie est sélectionnée
    if selected_category:
        games = games.filter(category__iexact=selected_category)

    # Filtrer par mot-clé de recherche si un mot-clé est fourni
    if search_keyword:
        games = games.filter(title__icontains=search_keyword)

    # Filtrer par fourchette de prix
    games = games.filter(price__lte=max_price)

    # Obtenir toutes les catégories disponibles pour la liste déroulante
    categories = VideoGame.objects.values_list('category', flat=True).distinct()

    return render(request, 'djangoProject/shop.html', {
        'games': games,
        'categories': categories,
        'search_keyword': search_keyword,
        'selected_category': selected_category,
        'max_price': max_price
    })




def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('shop')  # Rediriger l'utilisateur après la connexion
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'djangoProject/login.html', {'form': form})


# ViewSet for VideoGames (No authentication required)
def product_detail(request, id):
    game = get_object_or_404(VideoGame, id=id)
    return render(request, 'djangoProject/product-details.html', {'game': game})
class VideoGameViewSet(viewsets.ModelViewSet):
    queryset = VideoGame.objects.all()
    serializer_class = VideoGameSerializer
    permission_classes = [permissions.AllowAny]  # Accessible à tout le monde

# Views for Cart (Requires authentication)
class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Cart.objects.get(user=self.request.user)

class CartItemView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cart = Cart.objects.get(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def perform_create(self, serializer):
        cart = Cart.objects.get(user=self.request.user)
        serializer.save(cart=cart)

# ViewSet for Orders (Requires authentication)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        cart = Cart.objects.get(user=self.request.user)
        # Calculer le total des prix dans le panier
        total_price = sum([item.game.price * item.quantity for item in cart.items.all()])
        # Créer la commande
        order = serializer.save(user=self.request.user, total_price=total_price)
        # Ajouter les items du panier à la commande
        for item in cart.items.all():
            OrderItem.objects.create(order=order, game=item.game, quantity=item.quantity)
        # Vider le panier après validation de la commande
        cart.items.all().delete()

from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Crée un nouvel utilisateur
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')  # Redirige vers la page de connexion
    else:
        form = CustomUserCreationForm()
    return render(request, 'djangoProject/register.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('index')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm  # Assure-toi d'importer tes formulaires


def auth_view(request):
    if request.method == 'POST':
        # Traitement du formulaire d'inscription
        if 'signup' in request.POST:
            form_signup = CustomUserCreationForm(request.POST)
            if form_signup.is_valid():
                form_signup.save()  # Enregistre le nouvel utilisateur
                messages.success(request, 'Your account has been created successfully!')
                return redirect('auth')  # Redirige vers la même page après l'inscription
            else:
                messages.error(request, 'Please correct the errors below.')

        # Traitement du formulaire de connexion
        elif 'login' in request.POST:
            form_login = CustomAuthenticationForm(data=request.POST)
            if form_login.is_valid():
                username = form_login.cleaned_data.get('username')
                password = form_login.cleaned_data.get('password')
                user = authenticate(username=username, password=password)  # Authentifie l'utilisateur
                if user is not None:
                    login(request, user)  # Connecte l'utilisateur
                    return redirect('shop')  # Redirige vers la page shop après connexion
                else:
                    messages.error(request, 'Invalid username or password')

    # Formulaires par défaut pour l'affichage
    form_signup = CustomUserCreationForm()
    form_login = CustomAuthenticationForm()

    return render(request, 'djangoProject/auth.html', {
        'form_signup': form_signup,
        'form_login': form_login,
    })