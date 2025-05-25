from django.urls import path
from . import views
from .views import BlogCreateView, BlogUpdateView, BlogDeleteView,CustomLoginView
from django.contrib.auth import views as auth_views






urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='post_list'),

    path('post/new/', BlogCreateView.as_view(), name='post_create'),  

    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/edit/', BlogUpdateView.as_view(), name='post_edit'),
    path('post/<slug:slug>/delete/', BlogDeleteView.as_view(), name='post_delete'),

    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),

]

