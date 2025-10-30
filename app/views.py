from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegisterForm
from .tasks import send_welcome_email

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # optional: authenticate + login immediately
            user = authenticate(username=user.username, password=request.POST["password"])
            if user:
                login(request, user)
            # enqueue background welcome email
            send_welcome_email.delay(user.email or "", user.username)
            return render(request, "app/welcome_queued.html", {"email": user.email})
    else:
        form = RegisterForm()
    return render(request, "app/register.html", {"form": form})

class CustomLoginView(LoginView):
    template_name = "app/login.html"

class CustomLogoutView(LogoutView):
    template_name = "app/login.html"
