from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, TopicForm
from .models import Topic


def home(request):
    return render(request, 'main_app/home.html')


@login_required
def topic_index(request):
    topics = request.user.topics.all()
    return render(request, 'main_app/topic_index.html', {'topics': topics})


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('topic_index')
    else:
        form = SignupForm()
    return render(request, 'main_app/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('topic_index')
        return render(request, 'main_app/login.html', {'error': 'Invalid credentials'})
    return render(request, 'main_app/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def topic_create(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.user = request.user
            topic.save()
            return redirect('topic_index')
    else:
        form = TopicForm()
    return render(request, 'main_app/topic_create.html', {'form': form})


@login_required
def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk, user=request.user)
    return render(request, 'main_app/topic_detail.html', {'topic': topic})


@login_required
def topic_edit(request, pk):
    topic = get_object_or_404(Topic, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('topic_detail', pk=topic.pk)
    else:
        form = TopicForm(instance=topic)
    return render(request, 'main_app/topic_edit.html', {'form': form, 'topic': topic})


@login_required
def topic_delete(request, pk):
    topic = get_object_or_404(Topic, pk=pk, user=request.user)
    if request.method == 'POST':
        topic.delete()
        return redirect('topic_index')
    return render(request, 'main_app/topic_confirm_delete.html', {'topic': topic})
