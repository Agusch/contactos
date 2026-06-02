from django.urls import path
from .views import ContactoCreateView, ContactoUpdateView, ContactoListView, ContactoDeleteView

urlpatterns = [
    path('crear', ContactoCreateView.as_view(), name='contacto-create'),
    path('<int:id>/editar', ContactoUpdateView.as_view(), name='contacto-update'),
    path('filtrar', ContactoListView.as_view(), name='contacto-filter'),
    path('<int:id>/eliminar', ContactoDeleteView.as_view(), name='contacto-eliminar')
]