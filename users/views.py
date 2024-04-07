from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your views here.
@login_required
def home(request):
    return render(request, 'users/home.html')


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if '@' in username:
            user_exists = User.objects.filter(email=username).exists()
        else:
            user_exists = User.objects.filter(username=username).exists()

        if not user_exists:
            messages.error(request, 'Invalid Email or Username')
            return redirect('login')

        # if not User.objects.filter(username=username).exists() or User.objects.filter(email=username).exists():
        #     messages.error(request, 'Invalid Email or Username')
        #     return redirect('login')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('login')
        else:
            login(request, user)
            return redirect('home')
    return render(request, 'users/login.html')



def registerPage(request):
    if request.method == 'POST':
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            validate_password(password)
        
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email used already')
                return redirect('register')

            user = User.objects.create_user(
                first_name = firstName,
                last_name = lastName,
                username = username,
                email = email
            )

            user.set_password(password)
            user.save()
            messages.success(request, 'Your account created successfully.')
            return redirect('login')

        except ValidationError as e:
            for message in e.messages:
                messages.error(request, message)
            return redirect('register')
        except:
            return redirect('register')
 
    return render(request, 'users/register.html')


def logoutPage(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')


def deletePage(request, pk):
    if request.method == 'POST':
        user = User.objects.get(id=pk)
        user.delete()
        return redirect('login')
    