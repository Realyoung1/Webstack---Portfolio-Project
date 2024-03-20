from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
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