from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from uteis import utils

from . import models
from perfil.models import Perfil
import requests

# Create your views here.

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 5
    ordering = ['-id']

class Busca(ListaProdutos):
    def get_queryset(self, *args, **kwargs):
        termo = self.request.GET.get("termo") or self.request.session['termo']
        qs = super().get_queryset(*args, **kwargs)

        if not termo:
            return qs
        
        self.request.session['termo'] = termo

        qs = qs.filter(
            Q(nome__icontains=termo) |
            Q(descricao_curta__icontains=termo) |
            Q(descricao_longa__icontains=termo)
        )

        self.request.session.save()
        return qs

class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        '''if self.request.session.get('carrinho'):
            del self.request.session['carrinho']
            self.request.session.save()'''

        http_referer = self.request.META.get('HTTP_REFERER', reverse('produto:lista'))
        variacao_id = self.request.GET.get('vid')
        produto_id = self.request.GET.get('vid2')
        
        

        if produto_id:

            produto = get_object_or_404(models.Produto, id=produto_id)
            produto_nome = produto.nome
            preco_unitario = produto.preco_marketing
            preco_unitario_promocional = produto.preco_marketing_promocional
            quantidade = 1
            slug = produto.slug
            imagem = produto.imagem
            if imagem:
                imagem = imagem.name
            else:
                imagem=''

            if produto.estoque < 1:
                messages.error(self.request, 'Estoque insuficiente')
                return redirect(http_referer)

            if not self.request.session.get('carrinho'):
                self.request.session['carrinho'] = {}
                self.request.session.save()

            carrinho = self.request.session['carrinho']

            

            if produto_id in list(carrinho.keys()):
                quantidade_carrinho = carrinho[produto_id]['quantidade']
                quantidade_carrinho += 1

                if produto.estoque < quantidade_carrinho:
                    messages.warning(self.request, f'Estoque insuficiente, temos apenas {produto.estoque} unidades de {produto_nome}')
                    return redirect(f'/{slug}')


                carrinho[produto_id]['quantidade'] = quantidade_carrinho
                carrinho[produto_id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
                carrinho[produto_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * quantidade_carrinho


            else:
                carrinho[produto_id] = {
                    'produto_id' : produto_id,
                    'produto_nome' : produto_nome,
                    'preco_unitario' : preco_unitario,
                    'preco_unitario_promocional' : preco_unitario_promocional,
                    'preco_quantitativo' : preco_unitario,
                    'preco_quantitativo_promocional' : preco_unitario_promocional,
                    'quantidade' : 1,
                    'slug' : slug,
                    'altura' : produto.altura,
                    'peso' : produto.peso,
                    'profundidade' : produto.profundidade,
                    'largura' : produto.largura,
                    'imagem' : imagem,
                }                
            self.request.session.save()

            messages.success(self.request, f'Produto {produto_nome} adicionado ao seu carrinho')
            return redirect(http_referer)


        if variacao_id == None:
            print('printei2')
            messages.error(self.request, 'Escolha uma opção')
            return redirect(http_referer)

        if not variacao_id:
            messages.error(self.request, 'Produto não existe')
            return redirect(http_referer)


        
        variacao = get_object_or_404(models.Variacao, id=variacao_id)
        variacao_id = f'1-{variacao_id}'
        variacao_estoque = variacao.estoque
        produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem
        if imagem:
            imagem = imagem.name
        else:
            imagem=''

        if variacao.estoque < 1:
            messages.error(self.request, 'Estoque insuficiente')
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            if variacao_estoque < quantidade_carrinho:
                messages.warning(self.request, f'Estoque insuficiente, temos apenas {variacao_estoque} unidades de {produto_nome} {variacao_nome}')
                return redirect(f'/{slug}')


            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * quantidade_carrinho


        else:
            carrinho[variacao_id] = {
                'produto_id' : produto_id,
                'produto_nome' : produto_nome,
                'variacao_nome' : variacao_nome,
                'variacao_id' : variacao_id,
                'preco_unitario' : preco_unitario,
                'preco_unitario_promocional' : preco_unitario_promocional,
                'preco_quantitativo' : preco_unitario,
                'preco_quantitativo_promocional' : preco_unitario_promocional,
                'quantidade' : 1,
                'slug' : slug,
                'altura' : produto.altura,
                'peso' : produto.peso,
                'profundidade' : produto.profundidade,
                'largura' : produto.largura,
                'imagem' : imagem,
            }
        self.request.session.save()
        messages.success(self.request, f'Produto {produto_nome} {variacao_nome} adicionado ao seu carrinho')
        return redirect(http_referer)


class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFER', reverse('produto:lista'))
        variacao_id = self.request.GET.get('vid')
        produto_id = self.request.GET.get('vid2')
        frete = self.request.session.get('frete')

        if not variacao_id and not produto_id:
            return redirect(http_referer)
        
        if not self.request.session.get('carrinho'):
            return redirect(http_referer)

        if variacao_id not in self.request.session['carrinho'] and produto_id not in self.request.session['carrinho']:
            return redirect(http_referer)

        if variacao_id:
            carrinho = self.request.session['carrinho'][variacao_id]
            
            context = {
            'carrinho': self.request.session.get('carrinho', {}),
            'frete': frete
            }

            messages.success(self.request, f'Produto {carrinho["produto_nome"]} {carrinho["variacao_nome"]} removido ao seu carrinho')
            del self.request.session['carrinho'][variacao_id]
            self.request.session.save()
            return render(self.request, 'produto/carrinho.html', context)
        else:
            carrinho = self.request.session['carrinho'][produto_id]

            context = {
            'carrinho': self.request.session.get('carrinho', {}),
            'frete': frete
            }

            del self.request.session['carrinho'][produto_id]
            self.request.session.save()

            if not self.request.session.get('carrinho'):
                messages.error(
                    self.request,
                    'Carrinho vazio.'
                )
                return redirect('produto:lista')

            messages.success(self.request, f'Produto {carrinho["produto_nome"]} removido ao seu carrinho')
            return render(self.request, 'produto/carrinho.html', context)
        

class Carrinho(View):
    def get(self, *args, **kwargs):
        
        # pego perfil para pegar o cep
        # implemento API
        # passo para o contexto os valores da API
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Cadastre-se antes de acessar o seu carrinho')
            return redirect('perfil:criar')

        perfil = get_object_or_404(Perfil.objects.filter(usuario=self.request.user))
    
        url = "https://www.melhorenvio.com.br/api/v2/me/shipment/calculate"

        payload = {
            "from": { "postal_code": f"{perfil.cep}" },
            "to": { "postal_code": "90570020" },
            "package": {
                "height": 4,
                "width": 12,
                "length": 17,
                "weight": 1
            }
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiMDQ2NjVjNjAyN2MyODVlMWQyOTc2MjY1OTZiNTE2ZGIwZTMyMDY4M2NjOGZlYTVjMDlkYmVhYzljZTJhZDVhNmI5ZTBlZDVjNTY2ZjE1YzIiLCJpYXQiOjE3MDg1MzY4ODYuODAwODQ3LCJuYmYiOjE3MDg1MzY4ODYuODAwODUsImV4cCI6MTc0MDE1OTI4Ni43ODgzMiwic3ViIjoiOWI2M2JiNjgtOTkyNi00YjYxLWI0MzgtZTcxZThjNDhmYTMwIiwic2NvcGVzIjpbInNoaXBwaW5nLWNhbGN1bGF0ZSJdfQ.WWYMSq0ys7MasoZkcC852JyHMattfAG_cuY9hqohMrd0S1blAKeoCNsU_oAMrfJrQy0h6fPe33dXQL74Jzzg3GD7KshT-zVB8yqPp7pqparBr4SmOUAjsSNgVYwmGxR4FOxl6ZtnDl5_eyQV7iVU_DZDAS1UUw6y2vyFDmk6pZgdxiyraCIr7X6zxHzWDMXiMQogk7YdmDyRN107hbFovxjVM2_dtNmLsz418QNjfI-op2YsHOhLZ--p8id-SIV9PA2DG3Zn4EoAGYCVYmDba5VF3wSUc0hhLWCIJjezN8ewXABwKrgOhqLPDUEfwn043fW2yLiR7yk2Kp6zNogoxDQjJFcRalEEOG7qQrxOkQO-aWeXPMr2kbg0BGK2mcIOKhulpoYswGi2iSPNMPpwzrKl1qv03FqF1r1CeLnNsVlfKIdQQ4Cjw7bItyaSuyHNzQAbk2-NNO2zbSGGoPTPFkG4fkHhMn5mH7EPl5_8j-8w3vsmrTESScNOAuQk9lAOhLaokRz7R2VwsHJg37PongP3BFqdUo2ZESnMKfG9WSYCraO9jrBi3U2kF-mKFES-A9m5xfVjxWUWh3S4zdoU95u4O7YrkXbMR0IMV9M6Acl40YX5_NFbC9IFLgl5ZA5XiNWThRV1gLjjBTD4qZXzgbjZYTveN6syv3XmpcyIwXA",
            "User-Agent": "Aplicação pedrobg2707@gmail.com"
        }

        retorno = requests.post(url, json=payload, headers=headers).json()

        lista_de_transportadoras_valores = [ item for item in retorno if 'price' in item]
        lista_de_transportadoras_nomes = [ preco['name'] for preco in lista_de_transportadoras_valores]
        lista_de_transportadoras_valores = [ preco['price'] for preco in lista_de_transportadoras_valores]
        empresa_frete = lista_de_transportadoras_nomes[0]
        valor_frete = lista_de_transportadoras_valores[0]

        carrinho = self.request.session.get('carrinho', {})

        total_carrinho = sum([total_quant['preco_quantitativo'] for total_quant in carrinho.values()]) + float(valor_frete)

        frete = self.request.session.get('frete', {})
        self.request.session['frete'] = round(float(valor_frete), 2)
        
        self.request.session.save()

        #print(self.request.session.get('frete', {}))

        context = {
            'carrinho': self.request.session.get('carrinho', {}),
            'frete' : round(float(valor_frete), 2)
        }

        return render(self.request, 'produto/carrinho.html', context)


class ResumoDaCompra(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        perfil = Perfil.objects.filter(usuario=self.request.user).exists()

        if not perfil:
            messages.error(
                self.request,
                'Usuário sem perfil. Atualize seus dados.'
            )
            return redirect('perfil:criar')



        contexto = {
            'usuario': self.request.user,
            'carrinho': self.request.session['carrinho'],

        }

        return render(self.request, 'produto/resumodacompra.html', contexto)