from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse

# Create your views here.
class PagarPedido(View):
    def get(self, *args, **kwargs):
        return HttpResponse('PagarPedido')

class SalvarPedido(View):
    def get(self, *args, **kwargs):
        return HttpResponse('FecharPedido')

class DetalhesPedido(View):
    def get(self, *args, **kwargs):
        return HttpResponse('DetalhesPedido')
