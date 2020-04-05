from django.db import models

# Create your models here.
class Actividades(models.Model):
    nombreTarea = models.CharField(max_length=100)
    tiempoTarea = models.IntegerField()
    tiempofinal = models.IntegerField()
    fechaTarea = models.DateField()

class User(models.Model):
    nombreUser = models.CharField(max_length=100)
    dni = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    mail = models.CharField(max_length=100)

class Memorial(models.Model):
    nombreDefu = models.CharField(max_length=100)
    birth = models.DateField()
    defunct = models.DateField()
    description = models.CharField(max_length=300)
    public = models.IntegerField()
    city = models.CharField(max_length=100)
    dniAlta = models.CharField(max_length=100)

class photo(models.Model):
    url = models.CharField(max_length=100)
    dniAlta = models.CharField(max_length=100)
    nombreDefu = models.CharField(max_length=100)