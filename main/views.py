from django.shortcuts import render, redirect
from .models import Product, Rating, Favorite
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Avg


@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('products')
    else:
        form = ProductForm()

    return render(request, 'main/create.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('products')

    return render(request, 'main/login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'main/register.html', {
                'error': 'Такий користувач уже існує'
            })

        User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'main/register.html')


def products(request):
    products = Product.objects.annotate(avg_rating=Avg('ratings__score')).order_by('-avg_rating', '-created_at')

    search = request.GET.get('search')
    if search:
        products = products.filter(name__icontains=search)

    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, 'main/products.html', {
        'products': products
    })


def user_logout(request):
    if request.method == 'POST':
        logout(request)
    return redirect('login')


@login_required
def profile(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'main/profile.html', {'favorites': favorites})


def home(request):
    context = {
        'title': 'Головна сторінка',
        'description': 'Ласкаво просимо на мій навчальний Django-сайт.',
        'topics': ['Шаблони', 'Static', 'Авторизація', 'Моделі', 'Форми']
    }
    return render(request, 'main/home.html', context)


def about(request):
    context = {
        'title': 'Про сайт',
        'description': 'Цей сайт створений у межах практичної роботи з Django.'
    }
    return render(request, 'main/about.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    avg_rating = product.ratings.aggregate(avg=Avg('score'))['avg']

    user_rating = None
    is_favorite = False

    if request.user.is_authenticated:
        rating_obj = product.ratings.filter(user=request.user).first()
        if rating_obj:
            user_rating = rating_obj.score
        is_favorite = Favorite.objects.filter(product=product, user=request.user).exists()

    return render(request, 'main/product_detail.html', {
        'product': product,
        'avg_rating': avg_rating,
        'user_rating': user_rating,
        'is_favorite': is_favorite,
    })


@login_required
def rate_product(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        score = int(request.POST.get('score', 0))
        if 1 <= score <= 5:
            Rating.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={'score': score}
            )
    return redirect('product_detail', pk=pk)


@login_required
def toggle_favorite(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        fav, created = Favorite.objects.get_or_create(product=product, user=request.user)
        if not created:
            fav.delete()
    return redirect('product_detail', pk=pk)


def search_autocomplete(request):
    query = request.GET.get('q', '')
    results = []
    if len(query) >= 1:
        query_lower = query.lower()
        all_ids = [p.id for p in Product.objects.only('id', 'name') if query_lower in p.name.lower()]
        products = Product.objects.filter(id__in=all_ids)[:8]
        results = [
            {
                'id': p.id,
                'name': p.name,
                'price': str(p.price),
                'category': p.get_category_display(),
            }
            for p in products
        ]
    return JsonResponse({'results': results})