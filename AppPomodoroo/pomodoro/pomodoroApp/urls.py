from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	path('', views.index, name='index'),
    url('añadirusuario', views.add_user, name='añadirusuario'),
    url('añadirMemorial', views.add_memoria, name='añadirMemorial'),
    url('altaMemorial', views.altaMemorial, name='altaMemorial'),
    url('principal', views.principal, name='principal'),
    url('searcher', views.search, name='searcher'),
    url('publicpage', views.public, name='publicpage'),
    url('login', views.login, name='login'),
    url('logout', views.logout, name='logout')
]