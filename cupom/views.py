from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib import messages
from . import models
from uteis import utils

# Create your views here.
class AssimilaCupom(View):
    def get(self, *args, **kwargs):
        cupom = self.request.GET.get('cupom')
        carrinho = self.request.session.get('carrinho')
        frete = self.request.session.get('frete')
        total_carrinho_mais_frete = utils.cart_totals_mais_frete(carrinho, frete)
        float_total_carrinho_mais_frete = float(total_carrinho_mais_frete.replace('R$ ', '').replace(',', '.'))

        try:
            # Use get() instead of filter()
            cupom_de_desc = models.Cupom.objects.get(name=cupom)
            if not self.request.session.get('cupom'):
                self.request.session['cupom'] = {}
            
            cupom_salvo = self.request.session['cupom']
            
            if len(list(cupom_salvo.values())) >= 1:
                total_com_desconto = float_total_carrinho_mais_frete - float_total_carrinho_mais_frete*cupom_de_desc.desconto

        
                contexto = {
                    'cupom' : cupom_de_desc,
                    'desconto': cupom_de_desc.desconto*100,
                    'total_com_desconto' : total_com_desconto,
                    'carrinho' : carrinho,
                    'frete' : frete
                }
                self.request.session.save()
                messages.error(self.request, f'Você já aplicou um cupom {self.request.session["cupom"]}')
                return render(self.request, 'produto/carrinho.html', contexto)

            cupom_salvo[cupom_de_desc.pk] = {
                'cupom_name': cupom_de_desc.name,
                'cupom_desconto': cupom_de_desc.desconto
            }

            self.request.session.save()

            total_com_desconto = float_total_carrinho_mais_frete - float_total_carrinho_mais_frete*cupom_de_desc.desconto
            print(list(cupom_salvo.values()))
            messages.success(self.request, f'Cupom aplicado com sucesso')

        except models.Cupom.DoesNotExist:
            messages.error(self.request, 'Cupom not found.')
            return redirect('produto:carrinho')
        
        contexto = {
            'cupom' : cupom_de_desc,
            'desconto': cupom_de_desc.desconto*100,
            'total_com_desconto' : total_com_desconto,
            'carrinho' : carrinho,
            'frete' : frete
        }
        return render(self.request, 'produto/carrinho.html', contexto)
    
class RemoverCupom(View):
    def get(self, *args, **kwargs):
        cupom = self.request.GET.get('cupom')
        carrinho = self.request.session.get('carrinho')
        frete = self.request.session.get('frete')
        total_carrinho_mais_frete = utils.cart_totals_mais_frete(carrinho, frete)
        float_total_carrinho_mais_frete = float(total_carrinho_mais_frete.replace('R$ ', '').replace(',', '.'))

        if self.request.session.get('cupom'):
            # Use get() instead of filter()
            del self.request.session['cupom']
            self.request.session.save()
            messages.success(self.request, f'Cupom removido com sucesso')
        else:
            messages.error(self.request, 'Cupom not found.')
            return redirect('produto:carrinho')
        contexto = {
            'carrinho' : carrinho,
            'frete' : frete
        }
        return render(self.request, 'produto/carrinho.html', contexto)