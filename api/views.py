from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from .serializers import ContactoSerializer, DireccionSerializer, TelefonoSerializer, InformacionSerializer, CreateSerializer
from django.shortcuts import get_object_or_404
from .models import Contacto
from rest_framework.pagination import PageNumberPagination


class ContactoCreateView(APIView):

    def post(self, request):
        data_limpia = {}

        try:
            # 2. Extraemos y parseamos los JSON que vienen como strings
            # Usamos .get() directo de request.data para evitar problemas de copia
            data_limpia["contacto"] = json.loads(request.data.get("contacto", "{}"))
            data_limpia["direccion"] = json.loads(request.data.get("direccion", "{}"))
            data_limpia["telefonos"] = json.loads(request.data.get("telefonos", "[]"))
            
        except (json.JSONDecodeError, TypeError):
            return Response(
                {
                    "error": (
                        "Los campos contacto, direccion y telefonos "
                        "deben enviarse como JSON válido."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Extraemos el archivo de la fotografía si existe
        if "fotografia" in request.data:
            data_limpia["fotografia"] = request.data["fotografia"]

        # 4. Pasamos el diccionario nativo al serializer
        serializer = CreateSerializer(data=data_limpia)

        if serializer.is_valid():
            contacto = serializer.save()
            return Response(
                {
                    "id": contacto.id,
                    "mensaje": "Contacto creado correctamente"
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class ContactoUpdateView(APIView):
    def put(self, request, id):
        contacto_instancia = get_object_or_404(Contacto, pk=id)
        data_limpia = {}
        try:
            if "contacto" in request.data:
                data_limpia["contacto"] = json.loads(request.data.get("contacto"))
            if "direccion" in request.data:
                data_limpia["direccion"] = json.loads(request.data.get("direccion"))
            if "telefonos" in request.data:
                data_limpia["telefonos"] = json.loads(request.data.get("telefonos"))
                
        except (json.JSONDecodeError, TypeError):
            return Response(
                {"error": "Los campos enviados deben ser JSON válidos."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if "fotografia" in request.data:
            data_limpia["fotografia"] = request.data["fotografia"]

        # 2. Llamamos al serializer pasándole la instancia, la data y el partial=True
        serializer = CreateSerializer(contacto_instancia, data=data_limpia, partial=True)

        if serializer.is_valid():
            contacto_actualizado = serializer.save()
            return Response(
                {
                    "id": contacto_actualizado.id,
                    "mensaje": "Contacto actualizado correctamente."
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactoDeleteView(APIView): 
    def delete(self, request, id): 
        contacto_instancia = get_object_or_404(Contacto, pk=id)
        contacto_instancia.delete()
        return Response(
            {"message": "Contacto eliminado correctamente"}, 
            status=status.HTTP_200_OK
        )



class Pagination(PageNumberPagination):
    page_query_param = 'page'          
    page_size_query_param = 'size'     
    page_size = 10                     
    max_page_size = 100

class ContactoListView(APIView):
    pagination_class = Pagination

    def get(self, request):
        nombre_filter = request.query_params.get('nombre', None)
        telefono_filter = request.query_params.get('telefono', None)
        queryset = Contacto.objects.all()

        #Filtro nombre
        if nombre_filter:
            queryset = queryset.filter(nombre__icontains=nombre_filter)

        #Filtro numero telefono
        if telefono_filter:
            # Filtramos por el número en la relación anidada y evitamos duplicados
            queryset = queryset.filter(telefonos__numero__icontains=telefono_filter).distinct()

        queryset = queryset.prefetch_related('direccion','telefonos')

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        
        if page is not None:
            serializer = InformacionSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # Caso por defecto (sin paginación)
        serializer = InformacionSerializer(queryset, many=True)
        return Response(serializer.data)