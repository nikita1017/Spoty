from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import *

def auth(request):
    if request.method == 'POST':

        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print("OK")
                return redirect("index")
            else:
                print("Неверное имя пользователя или пароль.")
        else:
            print("Неверное имя пользователя или пароль.")
    form = AuthenticationForm()
    return render(request, 'spotyapp/auth.html', {"login_form": form})
def index(request):
    context = {
        "posts": Post.objects.all(),
    }
    return render(request, 'spotyapp/index.html', context=context)
def reg(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'spotyapp/register.html', {"form": form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("index")
        else:
            return render(request, 'spotyapp/register.html', {})
        
def signOut(request):
    logout(request)
    return redirect("/")