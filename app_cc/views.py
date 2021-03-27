from django.shortcuts import render
import cx_Oracle
from django.db import transaction,connections
from datetime import datetime
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
from django.contrib.auth import login as auth_login,logout,authenticate
from django.urls import reverse
from django.shortcuts import render,redirect
from app_cc.models import *

# Create your views here.
def login(request):
	mensaje = ''
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('app_cc:lista_colaborador'))
	
	if request.method == 'POST':
		username = request.POST.get('usuario')
		contrasenia = request.POST.get('contrasenia')
		user = authenticate(username=username,password=contrasenia)
		if user is not None:
			if user.is_active:
				auth_login(request,user)
				return redirect('app_cc:lista_colaborador')
			else:
				mensaje = 'USUARIO INACTIVO'
				return render(request,'login.html',{'mensaje':mensaje})
		else:
			mensaje = 'USUARIO O CONTRASEÑA INCORRECTA'
			return render(request,'login.html',{'mensaje':mensaje})
	return render(request,'login.html',{'mensaje':mensaje})

def cerrar_sesion(request):
	logout(request)
	return HttpResponseRedirect(reverse('app_cc:login'))


def index(request):
	consulta = Colaborador.objects.all()
	generos = Genero.objects.all()
	data = {'lista_colaborador':consulta,'generos':generos}
	return render(request, "index.html",data)
#    try:
#        conexion=cx_Oracle.connect("jaguaroracle", "Jaguar2021", "173.249.59.89:1521/xe")
#    except Exception as error:
#        print ("nel .Error: "+error)
#    else: 
#        print("Si!!!!")

def lista_colaborador(request):
	consulta = Colaborador.objects.all()
	generos = Genero.objects.all()
	data = {'lista_colaborador':consulta,'generos':generos}
	return render(request,'index.html',data)


def registrar_colaborador(request):
	guardar_editar = True
	generos = Genero.objects.all()
	ret_data,query_colaborador,errores = {},{},{}

	if request.method == 'POST':
		print("ESTAMOS EN EL METODO POST")
		ret_data['identificacion'] = request.POST.get('identificacion')
		ret_data['nombres'] = request.POST.get('nombres')
		ret_data['apellidos'] = request.POST.get('apellidos')
		ret_data['telefono'] = request.POST.get('telefono')
		ret_data['fecha_nacimiento'] = request.POST.get('fecha_nacimiento')
		ret_data['genero'] = int(request.POST.get('genero'))
		if request.POST.get('identificacion') == '':
			errores['identificacion'] = "DEBES INGRESAR LA IDENTIDAD"
		else:
			query_colaborador['identificacion'] = request.POST.get('identificacion')
		
		if request.POST.get('nombres') == '':
			errores['nombres'] = "DEBES INGRESAR NOMBRES"
		else:
			query_colaborador['nombres'] = request.POST.get('nombres')

		query_colaborador['apellidos'] = request.POST.get('apellidos')
		query_colaborador['telefono'] = request.POST.get('telefono')
		query_colaborador['fecha_nacimiento'] = request.POST.get('fecha_nacimiento')
		query_colaborador['Genero'] = Genero.objects.get(pk=request.POST.get('genero'))

		if not errores:
			try:
				colaborador = Colaborador(**query_colaborador)
				colaborador.save()
			except Exception as e:
				transaction.rollback()
				print (e)
				errores['administrador'] =  e
				ctx = {'generos':generos,
						'errores':errores,
						'ret_data':ret_data,
						'guardar_editar':guardar_editar}
				return render(request,'registrar_colaborador.html',ctx)
			else:
				transaction.commit()
				return HttpResponseRedirect(reverse('app_cc:lista_colaborador'))
		else:
			ctx = {'generos':generos,
					'errores':errores,
					'ret_data':ret_data,
					'guardar_editar':guardar_editar}
			return render(request,'registrar_colaborador.html',ctx)
	else:
		print("ESTAMOS EN EL METODO GET")
		ctx = {'generos':generos,'guardar_editar':guardar_editar}
		return render(request,'registrar_colaborador.html',ctx)

def eliminar_colaborador(request,id_colaborador):
	eliminar = Colaborador.objects.get(pk=id_colaborador).delete()
	return HttpResponseRedirect(reverse('app_cc:lista_colaborador'))

def modificar_colaborador(request,id_colaborador):
	consulta = Colaborador.objects.all()
	generos = Genero.objects.all()
	guardar_editar = False
	colaborador = Colaborador.objects.get(pk=id_colaborador)
	ret_data,query_colaborador,errores = {},{},{}

	if request.method=='POST':
		print("aqui va modificar")

		if request.POST.get('identificacion') == '' or request.POST.get('nombres') == '' or request.POST.get('apellidos') == '' or request.POST.get('telefono') == '' or request.POST.get('fecha_nacimiento') == '' or int(request.POST.get('genero')) == 0:
			errores['identificacion'] = "HAY ERRORES"

		if not errores:
			
			try:
				colaborador = Colaborador.objects.filter(pk=id_colaborador).update(identificacion=request.POST.get('identificacion'),
																					nombres=request.POST.get('nombres'),
																					apellidos=request.POST.get('apellidos'),
																					telefono=request.POST.get('telefono'),
																					fecha_nacimiento=request.POST.get('fecha_nacimiento'),
																					genero=request.POST.get('genero')
																				)

			except Exception as e:
				print(e )
				return HttpResponseRedirect(reverse('app_cc:lista_colaborador')+"?error")
			else:
				return HttpResponseRedirect(reverse('app_cc:lista_colaborador'))
		else:
			return HttpResponseRedirect(reverse('app_cc:lista_colaborador')+"?error")
	else:
		return HttpResponseRedirect(reverse('app_cc:lista_colaborador'))
