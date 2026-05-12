from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Topic, Note, Tag


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('name', 'description', 'status')


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)


class NoteForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget(years=range(1990, 2030)))

    class Meta:
        model = Note
        fields = ('date', 'content', 'reference')
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'What did you learn or work on today?'}),
            'reference': forms.Textarea(attrs={'placeholder': 'Links, books, notes to revisit…', 'rows': 3}),
        }
