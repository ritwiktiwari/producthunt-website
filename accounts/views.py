from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return render(request, 'products/index.html')
        else:
            context = {
                'error': 'Invalid Credentials'
            }
            return render(request, 'accounts/login.html', context)
    return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return render(request, 'products/index.html')

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                context = {
                    'error': 'User already exists',
                }
                return render(request, 'accounts/signup.html', context)
            else:
                if User.objects.filter(email=email).exists():
                    context = {
                    'error': 'Email already exists',
                }
                    return render(request, 'accounts/signup.html', context)
                else:
                    user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                    user.save()
                    auth.login(request, user)
                    return redirect('index')
        else:
            context = {
                'error': 'Passwords do not match'
            }
            return render(request, 'accounts/signup.html', context)
    return render(request, 'accounts/signup.html')