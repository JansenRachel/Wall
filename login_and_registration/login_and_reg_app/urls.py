from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index),
    path('new_user', views.new_user),
    path('login', views.login),
    path('sucessful_login', views.sucessful_login),
    path('logout', views.logout),

    path('new_post', views.new_post),
    path('new_comment', views.new_comment)
]