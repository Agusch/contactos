# API de Contactos

Esta es una API REST desarrollada con **Django** y **Django REST Framework (DRF)** para la gestión y filtrado optimizado de contactos, direcciones y teléfonos. El proyecto incluye paginación personalizada y consultas a la base de datos.

---

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:
* Python 3.10 o superior
* Git

---

## Instalación y Configuración Local

Para cargar el proyecto de manera local previamente debe crear su entorno virtual en python y activarlo. 
Despues dentro del del proyecto seguir los siguientes pasos.

### 1. Configurar las Variables de Entorno
Crea un archivo llamado `.env` en la raíz del proyecto y añade la configuración para la conexión a tu Base de Datos. 

**Ejemplo de contenido (`.env`):**

``env
DB_NAME=agenda
DB_USER=postgres
DB_PASSWORD=admin
DB_HOST=localhost
DB_PORT=5432``


### Instalar las dependencias 
pip install -r requirements.txt

### Hacer migraciones 
python manage.py makemigrations catalogos

python manage.py makemigrations api

python manage.py migrate catalogos

python manage.py migrate api

### LLenar catalogos
python manage.py seed

## Crear carpeta "media" en el directorio raiz del proyecto

### Cargar el postman collection para hacer pruebas
