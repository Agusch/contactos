from django.core.management.base import BaseCommand
from catalogos.models import CatEstados, CatTiposTelefono


class Command(BaseCommand):
    help = "Carga de catálogos"

    def handle(self, *args, **options):

        estados = [
            ("AGU", "Aguascalientes"),
            ("BCN", "Baja California"),
            ("BCS", "Baja California Sur"),
            ("CAM", "Campeche"),
            ("CHP", "Chiapas"),
            ("CHH", "Chihuahua"),
            ("COA", "Coahuila"),
            ("COL", "Colima"),
            ("DIF", "Ciudad de México"),
            ("DUR", "Durango"),
            ("GUA", "Guanajuato"),
            ("GRO", "Guerrero"),
            ("HID", "Hidalgo"),
            ("JAL", "Jalisco"),
            ("MEX", "México"),
            ("MIC", "Michoacán"),
            ("MOR", "Morelos"),
            ("NAY", "Nayarit"),
            ("NLE", "Nuevo León"),
            ("OAX", "Oaxaca"),
            ("PUE", "Puebla"),
            ("QUE", "Querétaro"),
            ("ROO", "Quintana Roo"),
            ("SLP", "San Luis Potosí"),
            ("SIN", "Sinaloa"),
            ("SON", "Sonora"),
            ("TAB", "Tabasco"),
            ("TAM", "Tamaulipas"),
            ("TLA", "Tlaxcala"),
            ("VER", "Veracruz"),
            ("YUC", "Yucatán"),
            ("ZAC", "Zacatecas")
        ]

        tipos = [
            (1, "Casa"),
            (2, "Teléfono móvil")
        ]

        for clave, nombre in estados:
            CatEstados.objects.update_or_create(
                clave=clave,
                defaults={
                    "nombre": nombre
                }
            )

        for id, nombre in tipos:
            CatTiposTelefono.objects.get_or_create(
                id=id,
                defaults={"nombre": nombre}
            )

        self.stdout.write(
            self.style.SUCCESS("Catálogos cargados correctamente")
        )