from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm  # Import your specific form
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm(request)

    return render(request, 'accounts/login.html', {'form': form})
def register_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already registered and logged in.")
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)  # Use your specific registration form
        if form.is_valid():
            user = form.save()  # This will save the user with all fields including user_type
            username = form.cleaned_data.get('username')
            login(request, user)  # Automatically log in the user after registration
            messages.success(request, f"Account created for {username}")
            return redirect('home')
        else:
            # If form is not valid, pass the form back to the template with errors
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = UserRegistrationForm()  # Use your specific registration form

    return render(request, 'accounts/register.html', {'form': form})
def profile_view(request):
    return render(request, 'accounts/profile.html')


@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')  # or return redirect('/')
