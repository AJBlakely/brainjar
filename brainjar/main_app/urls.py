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
]
