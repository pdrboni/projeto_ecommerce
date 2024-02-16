from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    path('', views.PagarPedido.as_view(), name='pagar'),
    path('salvarpedido/', views.SalvarPedido.as_view(), name='salvarpedido'),
    path('detalhe/', views.DetalhesPedido.as_view(), name='detalhespedido'),

]
