from django.shortcuts import render
from .models import Article
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
from django.contrib.auth import logout

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
        User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'main/register.html')

def articles(request):
    articles = Article.objects.all()
    return render(request, 'main/articles.html', {'articles': articles})

def user_logout(request):
    logout(request)
    return redirect('login')

def home(request):
   return render(request, 'main/home.html')


def about(request):
   return render(request, 'main/about.html')



# Create your views here.
