from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('topics/', views.topic_index, name='topic_index'),
    path('topics/new/', views.topic_create, name='topic_create'),
    path('topics/<int:pk>/', views.topic_detail, name='topic_detail'),
    path('topics/<int:pk>/edit/', views.topic_edit, name='topic_edit'),
    path('topics/<int:pk>/delete/', views.topic_delete, name='topic_delete'),
    path('topics/<int:topic_pk>/tags/add/', views.topic_add_tag, name='topic_add_tag'),
    path('topics/<int:topic_pk>/tags/<int:tag_pk>/remove/', views.topic_remove_tag, name='topic_remove_tag'),

    path('topics/<int:topic_pk>/notes/add/', views.note_add, name='note_add'),
    path('notes/<int:note_pk>/edit/', views.note_edit, name='note_edit'),
    path('notes/<int:note_pk>/delete/', views.note_delete, name='note_delete'),

    path('tags/', views.tag_index, name='tag_index'),
    path('tags/<int:pk>/', views.tag_detail, name='tag_detail'),
]
