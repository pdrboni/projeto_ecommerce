from typing import Any
from django.db.models.query import QuerySet
from django.http.request import HttpRequest as HttpRequest
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from uteis import utils
import requests

from cupom.models import Cupom
from produto.models import Variacao, Produto
from .models import Pedido, ItemPedido
from perfil.models import Perfil

# Create your views here.

class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args: Any, **kwargs: Any):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(usuario=self.request.user)
        return qs


class PagarPedido(DispatchLoginRequiredMixin, DetailView):
    template_name = 'pedido/pagar.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_obj_name = 'pedido'

class SalvarPedido(View):
    template_name = 'pedido/pagar.html'
    

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Você precisa estar logado para finalizar a compra')
            return redirect('perfil:criar')
        
        if not self.request.session.get('carrinho'):
            messages.error(self.request, 'Carrinho vazio.')
            return redirect('produto:lista')
        
        carrinho = self.request.session.get('carrinho')

        carrinho_produtos_ids = [p if not p.startswith('1-') else None for p in carrinho ]
        carrinho_variacao_ids = [v[2:] if v.startswith('1-') else None for v in carrinho if v is not None ]
        bd_produtos = list(
            Produto.objects.filter(id__in=carrinho_produtos_ids)
        )
        bd_variacao = list(
            Variacao.objects.filter(id__in=carrinho_variacao_ids)
        )
        

        for variacao in bd_variacao:
            vid = f'1-{variacao.id}'
            estoque = variacao.estoque

            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unt = carrinho[vid]['preco_unitario']
            preco_unt_promo = carrinho[vid]['preco_unitario_promocional']

            error_msg_estoque = ''

            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_quantitativo'] = estoque * preco_unt
                carrinho[vid]['preco_quantitativo_promocional'] = estoque * preco_unt_promo

                error_msg_estoque = f'O produto {carrinho[vid]["produto_nome"]} {carrinho[vid]["variacao_nome"]} ultrapassou nosso estoque. Ajustamos as quantiades destes produtos no seu carrinho para a quantidade disponível em estoque.'

            if error_msg_estoque:
                messages.error(self.request, error_msg_estoque)
                self.request.session.save()
                return redirect('produto:carrinho')
            
        for produto in bd_produtos:
            pid = str(produto.id)
            estoque = produto.estoque

            qtd_carrinho = carrinho[pid]['quantidade']
            preco_unt = carrinho[pid]['preco_unitario']
            preco_unt_promo = carrinho[pid]['preco_unitario_promocional']

            error_msg_estoque = ''

            if estoque < qtd_carrinho:
                carrinho[pid]['quantidade'] = estoque
                carrinho[pid]['preco_quantitativo'] = estoque * preco_unt
                carrinho[pid]['preco_quantitativo_promocional'] = estoque * preco_unt_promo

                error_msg_estoque = f'O produto {carrinho[pid]["produto_nome"]} ultrapassou nosso estoque. Ajustamos as quantiades destes produtos no seu carrinho para a quantidade disponível em estoque.'

            if error_msg_estoque:
                messages.error(self.request, error_msg_estoque)
                self.request.session.save()
                return redirect('produto:carrinho')
        
        if self.request.session.get('cupom'):
            cupom = self.request.session.get('cupom')
            cupom_list = list(cupom.values())[0]
            cupom_name = cupom_list['cupom_name']
            cupom_de_desc = Cupom.objects.get(name=cupom_name)
            
        frete = self.request.session.get('frete')

        qtd_total_carrinho = utils.cart_total_qtd(carrinho)
        valor_total_carrinho = utils.cart_totals(carrinho)
        valor_total_carrinho_mais_frete = valor_total_carrinho + frete
        valor_total_carrinho_mais_frete_desconto = valor_total_carrinho_mais_frete - valor_total_carrinho_mais_frete*cupom_de_desc.desconto

        pedido = Pedido(
            usuario=self.request.user,
            total=valor_total_carrinho_mais_frete_desconto,
            status='C',
            qtd_total=qtd_total_carrinho,
            cupom_aplicado=cupom_de_desc or None
            )
        
        pedido.save()

        for k in carrinho.keys():
            if str(k).startswith('1-'):
                ItemPedido.objects.bulk_create(
                    [
                        ItemPedido(
                            pedido=pedido,
                            produto=carrinho[k]['produto_nome'],
                            produto_id=carrinho[k]['produto_id'],
                            variacao=carrinho[k]['variacao_nome'],
                            variacao_id=carrinho[k]['variacao_id'],
                            preco=carrinho[k]['preco_quantitativo'],
                            preco_promocional=carrinho[k]['preco_quantitativo_promocional'],
                            quantidade=carrinho[k]['quantidade'],
                            imagem=carrinho[k]['imagem'],
                        )
                            
                    ]
                )

            else:
                ItemPedido.objects.bulk_create(
                    [
                        ItemPedido(
                            pedido=pedido,
                            produto=carrinho[k]['produto_nome'],
                            produto_id=carrinho[k]['produto_id'],
                            preco=carrinho[k]['preco_quantitativo'],
                            preco_promocional=carrinho[k]['preco_quantitativo_promocional'],
                            quantidade=carrinho[k]['quantidade'],
                            imagem=carrinho[k]['imagem'],
                        )
                            
                    ]
                )
        del self.request.session['frete']
        del self.request.session['carrinho']
        return redirect(
            reverse(
                'pedido:pagar',
                kwargs={
                    'pk':pedido.pk
                }
            )
            )

class DetalhesPedido(DispatchLoginRequiredMixin, DetailView):
    model = Pedido
    context_object_name = 'pedido'
    template_name = 'pedido/detalhe.html'
    pk_url_kwarg = 'pk'
    
class Lista(DispatchLoginRequiredMixin, ListView):
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedido/lista.html'
    paginate_by = 10
    ordering = ['-id']
