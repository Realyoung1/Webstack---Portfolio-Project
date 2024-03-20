from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import get_user_model



def register(request):
    if request.method == 'POST':
         # Manually capture form data
        username = request.POST['username']
        email = request.POST['email']
        name = request.POST['name']
        gender = request.POST['gender']
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        # Check if the two passwords match
        if password != confirm_password:
            return HttpResponse("Passwords do not match!")

        # Additional validation can be added here (e.g., check if username already exists)

        # Create new user
        User = get_user_model()
        user = User.objects.create(username=username, email=email, password=make_password(password))
        
        # Assuming you have a profile model linked to the user where you want to store name and gender
        # You'll need to adjust this part according to how your profile model is set up
        user.name = name
        user.gender = gender
        user.save()

        messages.success(request, f'Account created for {username}!')
        return redirect('login')  # Assuming you have a 'login' url configured
    else:
        form = UserRegisterForm()
    return render(request, 'quiz_app/register.html', {'form': form})


def home(request):
    return render(request, 'quiz_app/home.html')

# Contact view
def contact(request):
    return render(request, 'quiz_app/contact.html')

# Login view
def login(request):
    return render(request, 'quiz_app/login.html')