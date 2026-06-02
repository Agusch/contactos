from rest_framework import serializers
from .models import Contacto, Telefono, Direccion
from catalogos.models import CatEstados, CatTiposTelefono
from django.db import transaction

class ContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        exclude = ['fotografia']
    def get_fotografia_nombre(self, obj):
        return obj.fotografia.name if obj.fotografia else None


class DireccionSerializer(serializers.ModelSerializer):
    estado = serializers.PrimaryKeyRelatedField(
        queryset=CatEstados.objects.all(),
        error_messages={
            'does_not_exist': 'El estado seleccionado no existe.',
            'incorrect_type': 'Debe proporcionar una clave de estado válida.'
        }
    )
    class Meta:
        model = Direccion
        exclude = ['contacto']
    
    def validate_contacto(self, value):
        qs = Direccion.objects.filter(contacto=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "El contacto ya tiene una dirección registrada."
            )
        return value
    

class TelefonoSerializer(serializers.ModelSerializer):
    tipo = serializers.PrimaryKeyRelatedField(
        queryset=CatTiposTelefono.objects.all(),
        error_messages={
            'does_not_exist': 'El tipo de teléfono seleccionado no existe.'
        }
    )
    
    def validate(self, attrs):
        tipo_enviado = attrs.get('tipo')
        
        # Todo lo quei viene en telefonos
        serializer_padre = self.root
        #Identificar si es cración o actualización
        if serializer_padre and getattr(serializer_padre, 'instance', None) is None:
            
            # Lista de telefonos a crear
            initial_data_padre = getattr(serializer_padre, 'initial_data', {})
            telefonos_en_peticion = initial_data_padre.get('telefonos', [])

            #Tipos de telefonos que vienen en el post
            coincidencias = 0
            for t in telefonos_en_peticion:
                if int(t.get('tipo')) == tipo_enviado.id:
                    coincidencias += 1
            
            # Si se encuentra más de una vez el mismo tipo en el array del POST, lo rebotamos
            if coincidencias > 1:
                raise serializers.ValidationError({
                    "tipo": f"No puedes registrar más de un teléfono de tipo '{tipo_enviado}' para este contacto."
                })

        return attrs
    class Meta:
        model = Telefono
        exclude = ['contacto']

class InformacionSerializer(serializers.Serializer):
    contacto = ContactoSerializer(read_only=True)
    direccion = DireccionSerializer(many=True, read_only=True)
    telefonos = TelefonoSerializer(many=True, read_only = True)


class CreateSerializer(serializers.Serializer):
    contacto = ContactoSerializer()
    direccion = DireccionSerializer()
    telefonos = TelefonoSerializer(many=True)
    fotografia = serializers.ImageField(required=False)

    def create(self, validated_data):

        with transaction.atomic():
            contacto_data = validated_data.pop('contacto')
            direccion_data = validated_data.pop('direccion')
            telefonos_data = validated_data.pop('telefonos')
            fotografia = validated_data.pop('fotografia', None)

            contacto = Contacto.objects.create(**contacto_data, fotografia=fotografia)

            Direccion.objects.create(
                contacto=contacto,
                **direccion_data
            )

            for telefono_data in telefonos_data:
                Telefono.objects.create(
                    contacto=contacto,
                    **telefono_data
                )

            return contacto
    
    def update(self, instance, validated_data):
        contacto_data = validated_data.pop('contacto', None)
        direccion_data = validated_data.pop('direccion', None)
        telefonos_data = validated_data.pop('telefonos', None)
        fotografia = validated_data.pop('fotografia', None)

        with transaction.atomic():
            # 1. Actualizar Contacto 
            if contacto_data:
                # Le pasamos la instancia actual y la nueva data parcial
                contacto_serializer = ContactoSerializer(instance, data=contacto_data, partial=True)
                contacto_serializer.is_valid(raise_exception=True)
                contacto_serializer.save()
            
            # Guardar fotografía si se envió
            if fotografia is not None:
                instance.fotografia = fotografia
                instance.save()

            # 2. Actualizar Dirección 
            if direccion_data:
                direccion_obj, _ = Direccion.objects.get_or_create(contacto=instance)
                direccion_serializer = DireccionSerializer(direccion_obj, data=direccion_data, partial=True)
                direccion_serializer.is_valid(raise_exception=True)
                direccion_serializer.save()

            # 3. Actualizar Teléfonos UNO POR UNO si esq ue se nvia el tipo en el bodi del request
            if telefonos_data is not None:
                telefonos_actuales = instance.telefonos.all()
                #Creamos mapa de tipos existentes en el registro
                telefonos_map = {t.tipo: t for t in telefonos_actuales}

                for telefono_recibido in telefonos_data:
                    tipo_tel = telefono_recibido.get('tipo')
                    telefono_recibido['tipo'] = tipo_tel.id
                    # Buscamos si el contacto ya tiene un teléfono con este tipo 
                    if tipo_tel in telefonos_map:
                        # Si ya existe, lo ACTUALIZAMOS pasando la instancia
                        telefono_existente = telefonos_map[tipo_tel]
                        telefono_serializer = TelefonoSerializer(
                            telefono_existente, 
                            data=telefono_recibido, 
                            partial=True
                        )
                    else:
                        # Si no existe, lo CREAMOS (no le pasamos instancia)
                        telefono_serializer = TelefonoSerializer(data=telefono_recibido)

                    #Validamos el serializer
                    telefono_serializer.is_valid(raise_exception=True)
                    
                    # Al guardar, le inyectamos manualmente el contacto al que pertenece
                    telefono_serializer.save(contacto=instance)

        return instance

