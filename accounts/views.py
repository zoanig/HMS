from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import UserForm
# Create your views here.

def user_login(request):
    if request.user.is_authenticated:
        return redirect("core:index")
    if request.method == 'POST':
        return
    return render(request)

def user_logout(request):
    pass    