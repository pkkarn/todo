from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User  # For: Django Models
from django.db import IntegrityError  # For Raising Unique User Name Error
from django.contrib.auth import login, logout, authenticate  #
from .forms import TodoForm
from .models import Todo
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
def signupuser(request):
    if request.method == "GET":
        return render(request, 'memo/signupuser.html',
                      {'form': UserCreationForm()})  # Someone Visit Web GET 200, And See Form
    else:
        # If they Fill form and Submit it Then It will be (POST) method, We add that info into database.
        if request.POST['password1'] == request.POST['password2']:  # It Checks enter password is write or not
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])  # create user account and password
                user.save()  # used to save created data into database
                login(request, user)  # Logged in
                return redirect('current')
            except IntegrityError:
                return render(request, 'memo/signupuser.html', {'form': UserCreationForm(),
                                                                'user_name_error': 'User Name Already Taken, Try Different One.'})
        else:
            return render(request, 'memo/signupuser.html',
                          {'form': UserCreationForm(), 'error': 'Password Didn\'t Match, Try Again.'})
            # Key always used to access value

@login_required
def logoutuser(request):
    if request.method == 'POST':  # Because Chrome start crawling and access all GET PAGE
        logout(request)
        return redirect('home')


def loginuser(request):
    if request.method == "GET":
        return render(request, 'memo/login.html',
                      {'form': AuthenticationForm()})  # Someone Visit Web GET 200, And See Form
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'memo/login.html',
                          {'form': AuthenticationForm(), 'error': 'Username Or Password Didn\'t Match'})
        else:
            login(request, user)  # Logged in
            return redirect('current')


def home(request):
    return render(request, "memo/home.html")

@login_required
def current(request):
    todos = Todo.objects.filter(user=request.user,
                                datecompleted__isnull=True)  # It means data should be requested user and date complete will be Falase
    return render(request, 'memo/current.html', {'todos': todos})

@login_required
def create(request):
    if request.method == 'GET':  # If visit == GET
        return render(request, 'memo/create.html', {'form': TodoForm()})
    else:  # Post: Submited
        try:
            form = TodoForm(request.POST)  # it will get all field enter in Form
            newtodo = form.save(commit=False)  # New To Do not to save in DB
            newtodo.user = request.user  # To tell requested user enter
            newtodo.save()  # Now it's sve it's to new use
            return redirect('current')
        except ValueError:
            return render(request, 'memo/create.html', {'form': TodoForm, 'error': 'Wrongly Entered Data'})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'memo/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)  # it will get all field enter in Form
            form.save()
            return redirect('current')
        except ValueError:
            return render(request, 'memo/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Bad Data Passed'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('current')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current')

@login_required
def completetodos(request):
    todos = Todo.objects.filter(user=request.user,
                                datecompleted__isnull=False).order_by('-datecompleted')  # It means data should be requested user and date complete will be Falase
    return render(request, 'memo/completed.html', {'todos': todos})
