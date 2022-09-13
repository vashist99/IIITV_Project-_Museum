from django.contrib import admin
from django.conf.urls import include, url
from App import views

app_name = "App"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.RegisterFormView.as_view(), name='register'),
    url(r'^login/$', views.LoginFormView.as_view(), name='login'),
    url(r'^logout/$', views.signout, name='logout'),
    url(r'^about-us/$', views.AboutUs, name='aboutus'),
    url(r'^project-form/$', views.ProjectFormView.as_view(), name='project-form'),
    url(r'^project-detail/(?P<pk>[0-9]+)/', views.project_detail, name='project-detail'),
    url(r'^leaderboard/$', views.leaderboard, name='leaderboard'),
    url(r'^liked/(?P<pk>[0-9]+)/', views.liked, name='liked'),
    url(r'^delete/(?P<pk>[0-9]+)/', views.delete, name='delete')

]
