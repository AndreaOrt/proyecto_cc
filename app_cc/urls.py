from django.urls import path
from . import views

app_name = 'app_cc'

urlpatterns = [
    path('index/', views.index, name="index"),
    path('listado/', views.lista_colaborador, name="lista_colaborador"),
    path('',views.login,name='login'),
  	path('salir',views.cerrar_sesion,name='cerrar_sesion'),
 	path('registrar/colaborador/',views.registrar_colaborador,name='registrar_colaborador'),
 	path('eliminar/colaborador/<int:id_motor>/',views.eliminar_colaborador,name='eliminar_colaborador'),
 	path('modificar/colaborador/<int:id_trabajo>/',views.modificar_colaborador,name='modificar_colaborador'),

]