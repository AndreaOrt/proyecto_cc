from django.db import models

# Create your models here.

class Genero(models.Model):
	descripcion_genero = models.CharField(max_length=100)

	def __str__(self):
		return "{}-{}".format(self.pk,self.descripcion_genero)


class Colaborador(models.Model):
	identificacion = models.CharField(max_length=20)
	nombres = models.CharField(max_length=50)
	apellidos = models.CharField(max_length=50)
	telefono = models.CharField(max_length=20)
	fecha_nacimiento = models.DateField(auto_now_add=False)
	Genero =  models.ForeignKey(Genero, on_delete=models.CASCADE)
	

	def __str__(self):
		return "{}-{} {}".format(self.identificacion,self.nombres,self.telefono)



