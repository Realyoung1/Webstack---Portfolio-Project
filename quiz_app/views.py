from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout



def register(request):
    if request.method == 'POST':
         # Manually capture form data
        username = request.POST['username']
        email = request.POST['email']
        name = request.POST['name']
        gender = request.POST['gender']
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        User = get_user_model()
        
        #Checking if the email is already exist
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already exists. Please use a different email address.")
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists. Please use a different username.")
        
        # Check if the two passwords match
        if password != confirm_password:
            return HttpResponse("Passwords do not match!")
       
        user = User.objects.create(username=username, email=email, password=make_password(password))
        
        user.name = name
        user.gender = gender
        user.save()

        messages.success(request, f'Account created for {username}!')
        return redirect('login')  
    else:
        form = UserRegisterForm()
    return render(request, 'quiz_app/register.html', {'form': form})


def home(request):
    return render(request, 'quiz_app/home.html')

# Contact view
def contact(request):
    return render(request, 'quiz_app/contact.html')

# Login view
def user_login(request):
     if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')

        # Authenticating the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            # Redirect to a success page.
            return redirect('home')  
        else:
            # Return an 'invalid login' error message.
            messages.error(request, 'Invalid username or password.')

     return render(request, 'quiz_app/login.html')

def user_logout(request):
    logout(request)
    # Redirect to login page after logout
    return redirect('login')
