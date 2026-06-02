from django.db import models
from catalogos.models import CatEstados, CatTiposTelefono

class Contacto(models.Model):
    nombre = models.CharField(max_length= 60)
    apellido_paterno = models.CharField(max_length=120)
    apellido_materno = models.CharField(max_length=120)
    fotografia = models.ImageField(upload_to="fotografias/")
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return f'{self.nombre} {self.apellido_paterno} {self.apellido_materno}'

class Direccion(models.Model):
    contacto = models.ForeignKey(
        Contacto, 
        on_delete=models.CASCADE,
        related_name="direccion")
    estado = models.ForeignKey(CatEstados, on_delete=models.DO_NOTHING)
    municipio = models.CharField(max_length=255)
    colonia = models.CharField(max_length=255)
    calle = models.CharField(max_length=255)
    numero_exterior = models.CharField(max_length=10)
    numero_interior = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.calle} {self.numero_exterior}'

class Telefono(models.Model):
    contacto = models.ForeignKey(
        Contacto, 
        on_delete=models.CASCADE,
        related_name='telefonos')
    tipo = models.ForeignKey(CatTiposTelefono, on_delete=models.DO_NOTHING)
    alias = models.CharField(max_length=255)
    numero = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['contacto', 'tipo'], 
                name='unique_contacto_por_tipo_telefono'
            )
        ]
    
    def __str__(self):
        return f'{self.alias} : {self.numero}'

