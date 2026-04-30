from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404


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
    products = Product.objects.all()

    search = request.GET.get('search')
    if search:
        products = products.filter(name__icontains=search)

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
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    return render(request, 'main/profile.html')


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
    return render(request, 'main/product_detail.html', {'product': product})
