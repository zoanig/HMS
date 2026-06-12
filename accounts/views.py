from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import SignUPForm, LoginForm
# Create your views here.

def user_login(request):
    if request.user.is_authenticated:
        return redirect("core:index")
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect("core:index")
            else:
                form.add_error(None, "Invalid username or password.")
        return render(request, "login.html", {"form": form})    
    return render(request, "login.html", {"form": LoginForm()})

def user_logout(request):
    logout(request)
    return redirect("core:index")

def signUp_user(request):
    if request.user.is_authenticated:
        return redirect("core:index")
    if request.method == 'POST':
        form = SignUPForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("patients:new_profile")
        return render(request, "signup.html", {"form": form})

    return render(request, "signup.html", {"form": SignUPForm()})