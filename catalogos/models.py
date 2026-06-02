from django.db import models

class CatEstados(models.Model):
    clave = models.CharField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class CatTiposTelefono(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=20)
    def __str__(self):
        return self.nombre