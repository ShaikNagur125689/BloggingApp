from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.views import LoginView


@never_cache
@login_required
def post_list(request):
    query = request.GET.get('q', '')

    my_posts = BlogPost.objects.filter(author=request.user)
    other_posts = BlogPost.objects.exclude(author=request.user)

    if query:
        my_posts = my_posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
        other_posts = other_posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    my_posts = my_posts.order_by('-created_at')
    other_posts = other_posts.order_by('-created_at')

    my_page_number = request.GET.get('my_page')
    my_paginator = Paginator(my_posts, 5)
    my_page_obj = my_paginator.get_page(my_page_number)

    other_page_number = request.GET.get('other_page')
    other_paginator = Paginator(other_posts, 5)
    other_page_obj = other_paginator.get_page(other_page_number)

    return render(request, 'post_list.html', {
        'my_page_obj': my_page_obj,
        'other_page_obj': other_page_obj,
        'query': query
    })


@never_cache
@login_required
def post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'post_detail.html', {'post': post})


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    fields = ['title', 'content']
    template_name = 'post_form.html'
    success_url = reverse_lazy('post_list') 
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    fields = ['title', 'content']
    template_name = 'post_form.html'  

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


@never_cache
def signup(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@never_cache
def home(request):
    if request.user.is_authenticated:
        return redirect('post_list')  
    return render(request, 'home.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('post_list')
        return super().dispatch(request, *args, **kwargs)
