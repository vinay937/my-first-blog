from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django import forms
from .forms import UserRegistrationForm

def post_list(request):
	posts = Post.objects.filter(publish_date__lte=timezone.now()).order_by('publish_date')
	return render(request, 'blog/post_list.html', { 'posts' : posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})
# Create your views here.
def test(request):
    return render(request, 'blog/test.html')
def home(request):
    return render(request, 'blog/home.html')
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
    else:
        form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'form' : form})
