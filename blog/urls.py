from django.urls import path
from . import views
from django.conf.urls import url
from .views import home, register, test

urlpatterns = [
	path('', views.post_list, name='post_list'),
	path('post/<int:pk>/', views.post_detail, name='post_detail'),
	url(r'^$', home),
	url(r'^test/', views.upload, name='test'),
	url(r'^upload/', views.upload, name='upload'),
	url(r'^download/', views.download, name='download'),
    url(r'^register/', register),
]