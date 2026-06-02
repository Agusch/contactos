from rest_framework import serializers
from .models import CatEstados, CatTiposTelefono

class CatEstadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatEstados
        fields = '__all__'

class CatTipoTelefonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatTiposTelefono
        fields = '__all__'