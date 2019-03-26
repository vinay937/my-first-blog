from django.urls import path
from . import views
from django.conf.urls import url
from .views import home, register, test

urlpatterns = [
	path('', views.post_list, name='post_list'),
	path('post/<int:pk>/', views.post_detail, name='post_detail'),
	url(r'^$', home),
	url(r'^test/', test),
    url(r'^register/', register),
]