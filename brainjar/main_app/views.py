from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .forms import SignupForm, TopicForm, NoteForm, TagForm
from .models import Topic, Note, Tag


def home(request):
    return render(request, 'main_app/home.html')


@login_required
def topic_index(request):
    topics = request.user.topics.prefetch_related('tags').all()
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
    note_form = NoteForm()
    existing_tags = request.user.tags.exclude(pk__in=topic.tags.all())
    return render(request, 'main_app/topic_detail.html', {
        'topic': topic,
        'note_form': note_form,
        'existing_tags': existing_tags,
    })


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


@login_required
def topic_add_tag(request, topic_pk):
    topic = get_object_or_404(Topic, pk=topic_pk, user=request.user)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip().lower()
        if name:
            tag, _ = Tag.objects.get_or_create(user=request.user, name=name)
            topic.tags.add(tag)
    return redirect('topic_detail', pk=topic_pk)


@login_required
def topic_remove_tag(request, topic_pk, tag_pk):
    topic = get_object_or_404(Topic, pk=topic_pk, user=request.user)
    tag = get_object_or_404(Tag, pk=tag_pk, user=request.user)
    if request.method == 'POST':
        topic.tags.remove(tag)
    return redirect('topic_detail', pk=topic_pk)


@login_required
def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name'].strip().lower()
            Tag.objects.get_or_create(user=request.user, name=name)
            return redirect('tag_index')
    else:
        form = TagForm()
    return render(request, 'main_app/tag_create.html', {'form': form})


@login_required
def tag_index(request):
    tags = request.user.tags.annotate(topic_count=Count('topics')).order_by('name')
    return render(request, 'main_app/tag_index.html', {'tags': tags})


@login_required
def tag_detail(request, pk):
    tag = get_object_or_404(Tag, pk=pk, user=request.user)
    topics = tag.topics.filter(user=request.user).prefetch_related('tags')
    return render(request, 'main_app/tag_detail.html', {'tag': tag, 'topics': topics})


@login_required
def note_add(request, topic_pk):
    topic = get_object_or_404(Topic, pk=topic_pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.topic = topic
            note.save()
            return redirect('topic_detail', pk=topic_pk)
        return render(request, 'main_app/topic_detail.html', {'topic': topic, 'note_form': form})
    return redirect('topic_detail', pk=topic_pk)


@login_required
def note_edit(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk, topic__user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('topic_detail', pk=note.topic.pk)
    else:
        form = NoteForm(instance=note)
    return render(request, 'main_app/note_edit.html', {'form': form, 'note': note})


@login_required
def note_delete(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk, topic__user=request.user)
    topic_pk = note.topic.pk
    if request.method == 'POST':
        note.delete()
    return redirect('topic_detail', pk=topic_pk)
