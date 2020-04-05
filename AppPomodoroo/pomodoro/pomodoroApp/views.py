from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import date
from django.template import loader
from .models import User, Memorial, photo

#--Global--
usuarioActivo = User()

def index(request):
    context = {}
    return render(request,"pomodoroApp/index.html", context)

def logout(request):
    usuarioActivo = User()
    return index(request)

def login(request):
    global usuarioActivo
    # obtener los datos de la vista
    usermail = request.POST['emailUsuario']
    password = request.POST['passUsuario']
    try:
        objsuser = User.objects.get(mail=usermail)
        if objsuser.password == password:
            usuarioActivo.nombreUser = objsuser.nombreUser
            usuarioActivo.password = password
            usuarioActivo.mail = usermail
            usuarioActivo.dni = objsuser.dni
            return principal(request)
        else:
            # error
            template = loader.get_template("pomodoroApp/index.html")
            alar = "Usuario Incorrecto, Contraseña incorrecta"
            context = {
                "alarma": alar
            }
            return HttpResponse(template.render(context, request))
    except:
        # error
        template = loader.get_template("pomodoroApp/index.html")
        alar ="Usuario Incorrecto, Usuario no encontrado "
        context = {
            "alarma":alar
        }
        return HttpResponse(template.render(context, request))

def principal(request):
    global usuarioActivo
    template = loader.get_template("pomodoroApp/main.html")
    try:
        memorials = Memorial.objects.get(dniAlta=usuarioActivo.dni)
        otromem = Memorial.objects.all()
        context = {
            "memorials": memorials,
            "otrosM": otromem[0],
            "alarma":None
        }
    except:
        try:
            otromem = Memorial.objects.all()
            context = {
                "otrosM": otromem[0],
                "alarma":None
            }
        except:
            context = {
                "alarma": "No memorials in BD"
            }
    return HttpResponse(template.render(context, request))


def altaMemorial(request):
    global usuarioActivo
    context = {"usuarioActivo": usuarioActivo}
    return render(request,"pomodoroApp/altaMemorial.html", context)

def add_user(request):
    if request.method == 'PUT' or request.method == 'POST':
        username = request.POST['nombreAltaUsuario']
        password = request.POST['passAltaUsuario']
        email = request.POST['emailAltaUsuario']
        dni = request.POST['DNIAltaUsuario']
        permisousuario = False
        try:
            if username != '' and password != '' and email != '' and dni != '':
                useralta = User(nombreUser=username, password=password, mail=email,dni=dni)
                useralta.save()
                template = loader.get_template("pomodoroApp/index.html")
                alar = "Usuario correcto"
                context = {
                    "alarma": alar,
                    "usuarioActivo": usuarioActivo
                }
                return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template("pomodoroApp/index.html")
                alar = "Usuario Incorrecto, Introduza los campos correctamente"
                context = {
                    "alarma": alar,
                    "usuarioActivo": usuarioActivo
                }
                return HttpResponse(template.render(context, request))
        except:
            template = loader.get_template("pomodoroApp/index.html")
            alar = "Usuario Incorrecto, Introduza los campos correctamente"
            context = {
                "alarma": alar,
                "usuarioActivo": usuarioActivo
            }
            return HttpResponse(template.render(context, request))

    else:
        template = loader.get_template("myfilm/altausuarios.html")
        alar = "Usuario Incorrecto, Introduza los campos correctamente"
        context = {
            "alarma": alar,
            "usuarioActivo": usuarioActivo
        }
        return HttpResponse(template.render(context, request))

def add_memoria(request):
    global usuarioActivo
    if request.method == 'PUT' or request.method == 'POST':
        nombreDefu = request.POST['nombreAltaUsuario']
        birth = request.POST['nombreAltaUsuario']
        defunct = request.POST['nombreAltaUsuario']
        description = request.POST['nombreAltaUsuario']
        public = request.POST['nombreAltaUsuario']
        city = request.POST['nombreAltaUsuario']
        dniAlta = usuarioActivo.dni
        url = request.POST['url']
        try:
            if nombreDefu != '' and birth != '' and defunct != '' and description != '' and public != '' and city != '' and dniAlta != '' :
                if public != 'public':
                    npublic = 1
                else:
                    npublic = 0
                mem = Memorial(nombreDefu=nombreDefu, defunct=defunct, description=description,public=npublic,city = city,dniAlta =dniAlta,)
                mem.save()
                if url != '' :
                    foto = photo(dniAlta=dniAlta, nombreDefu=nombreDefu, url=url)
                    foto.save()

                template = loader.get_template("pomodoroApp/altaMemorial.html")
                alar = "Alta correcto"
                context = {
                    "alarma": alar,
                    "usuarioActivo": usuarioActivo
                }
                return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template("pomodoroApp/altaMemorial.html")
                alar = "Datos Incorrectos, Introduza los campos correctamente"
                context = {
                    "alarma": alar,
                    "usuarioActivo": usuarioActivo
                }
                return HttpResponse(template.render(context, request))
        except:
            template = loader.get_template("pomodoroApp/altaMemorial.html")
            alar = "Datos Incorrectos, Introduza los campos correctamente"
            context = {
                "alarma": alar,
                "usuarioActivo": usuarioActivo
            }
            return HttpResponse(template.render(context, request))

    else:
        template = loader.get_template("pomodoroApp/altaMemorial.html")
        alar = "Datos Incorrectos, Introduza los campos correctamente"
        context = {
            "alarma": alar,
            "usuarioActivo": usuarioActivo
        }
        return HttpResponse(template.render(context, request))

def search(request):
    global usuarioActivo
    template = loader.get_template("pomodoroApp/main.html")
    try:
        if request.POST['input_search'] != '':
            memorialselect = Memorial.objects.filter(nombreDefu=request.POST['input_search'])
            context = {
                "memorials": memorialselect,
            }
            return HttpResponse(template.render(context, request))
        else:
            try:
                otromem = Memorial.objects.all()
                context = {
                    "otrosM": otromem[0],
                    "alarma":None
                }
                return HttpResponse(template.render(context, request))
            except:
                context = {
                    "alarma": "No memorials in BD"
                }
                return HttpResponse(template.render(context, request))
    except:
       principal(request)

    return HttpResponse(template.render(context, request))

