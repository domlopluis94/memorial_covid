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
    global usuarioActivo
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
        photo1 = photo.objects.get(nombreDefu=memorials.nombreDefu)
        otromem = Memorial.objects.all()
        context = {
            "memorials": memorials,
            "photo1": photo1,
            "otrosM": otromem[0],
            "alarma":None,
            "usuarioActivo": usuarioActivo
        }
    except:
        try:
            otromem = Memorial.objects.all()
            context = {
                "otrosM": otromem[0],
                "alarma":None,
                "memorials": otromem[0],
                "usuarioActivo": usuarioActivo
            }
        except:
            context = {
                "otrosM": None,
                "memorials": None,
                "alarma": "No memorials in BD",
                "usuarioActivo": usuarioActivo
            }
    return HttpResponse(template.render(context, request))

def public(request):
    global usuarioActivo
    template = loader.get_template("pomodoroApp/public.html")
    memorials = Memorial.objects.filter(public=0)
    listafotos = []
    listmemorials = []
    for e in memorials:
            listmemorials.append(e)

    length = len(listmemorials)

    for i in range(length):
        photo1 = photo.objects.get(nombreDefu=listmemorials[i].nombreDefu)
        listafotos.append(photo1)

    union = zip(listmemorials,listafotos)
    try:
        context = {
            "listaPersonas": union,
            "listafotos": listafotos,
            "alarma": None,
            "sice":length,
            "usuarioActivo": usuarioActivo
        }

    except:
        try:
            otromem = Memorial.objects.all()
            context = {
                "listaPersonas": otromem[0],
                "alarma":"no hay publicos",
                "usuarioActivo": usuarioActivo
            }
        except:
            context = {
                "otrosM": None,
                "memorials": None,
                "alarma": "No memorials in BD",
                "usuarioActivo": usuarioActivo
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
        nombreDefu = request.POST['nombreDefu']
        birth = request.POST['birth']
        defunct = request.POST['defunct']
        description = request.POST['description']
        public = request.POST['public']
        city = request.POST['city']
        dniAlta = usuarioActivo.dni
        url = request.POST['url']
        try:
            if nombreDefu != '' and birth != '' and defunct != '' and description != '' and city != '':
                if public != 'Public':
                    npublic = 1
                else:
                    npublic = 0
                mem = Memorial(nombreDefu=nombreDefu, birth=birth,defunct=defunct, description=description, public=npublic,city=city, dniAlta=dniAlta)
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
                alar = "Datos Incorrectos, Introduza todos los campos correctamente"
                context = {
                    "alarma": alar,
                    "usuarioActivo": usuarioActivo
                }
                return HttpResponse(template.render(context, request))
        except:
            template = loader.get_template("pomodoroApp/altaMemorial.html")
            alar = "Datos Incorrectos, Introduza los campos correctamente" + dniAlta + nombreDefu
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
            photo1 = photo.objects.get(nombreDefu=memorialselect.nombreDefu)
            context = {
                "memorials": memorialselect,
                "usuarioActivo": usuarioActivo,
                "photo1":photo1
            }
            return HttpResponse(template.render(context, request))
        else:
            try:
                otromem = Memorial.objects.all()
                context = {
                    "otrosM": otromem[0],
                    "alarma":None,
                    "usuarioActivo": usuarioActivo
                }
                return HttpResponse(template.render(context, request))
            except:
                context = {
                    "alarma": "No memorials in BD",
                    "usuarioActivo": usuarioActivo
                }
                return HttpResponse(template.render(context, request))
    except:
       return principal(request)

    return HttpResponse(template.render(context, request))

