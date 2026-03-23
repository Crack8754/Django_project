from django.shortcuts import render, redirect
from .models import Article
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm


@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('articles')
    else:
        form = ArticleForm()

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
            return redirect('articles')

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


def articles(request):
    articles = Article.objects.all()
    return render(request, 'main/articles.html', {'articles': articles})


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
