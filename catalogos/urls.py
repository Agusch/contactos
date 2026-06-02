from django.urls import path
from .views import EstadosListView, TelefonosListView

urlpatterns = [
    path('estados', EstadosListView.as_view(), name='catalogo-estados'),
    path('tipo-telefono', TelefonosListView.as_view(), name='catalogo-telefonos'),
]