from rest_framework.views import APIView
from rest_framework.response import Response
from api.views import Pagination
from .serializers import CatEstadosSerializer, CatTipoTelefonoSerializer
from .models import CatTiposTelefono, CatEstados

class EstadosListView(APIView):
    pagination_class = Pagination

    def get(self, request):
        id_filter = request.query_params.get('id', None)
        nombre_filter = request.query_params.get('nombre', None)
        queryset = CatEstados.objects.all()

        #Filtro nombre
        if nombre_filter:
            queryset = queryset.filter(nombre__icontains=nombre_filter)

        #Filtro id
        if id_filter:
            queryset = queryset.filter(clave__icontains=id_filter)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        
        if page is not None:
            serializer = CatEstadosSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # Caso por defecto (sin paginación)
        serializer = CatEstadosSerializer(queryset, many=True)
        return Response(serializer.data)
    

class TelefonosListView(APIView):
    pagination_class = Pagination

    def get(self, request):
        queryset = CatTiposTelefono.objects.all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
    
        if page is not None:
            serializer = CatTipoTelefonoSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # Caso por defecto (sin paginación)
        serializer = CatTipoTelefonoSerializer(queryset, many=True)
        return Response(serializer.data)