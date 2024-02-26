def formata_preco(val):
    return f'R$ {val:.2f}'.replace('.', ',')

def cart_total_qtd(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])

def cart_totals(carrinho):
    return sum([
        item.get('preco_quantitativo_promocional') if item.get('preco_quantitativo_promocional') else item.get('preco_quantitativo') for item in carrinho.values()
    ])

def cart_totals_mais_frete(carrinho, frete=0):
    soma_carrinho = sum([
        item.get('preco_quantitativo_promocional') if item.get('preco_quantitativo_promocional') else item.get('preco_quantitativo') for item in carrinho.values()
    ])
    soma_carrinho_mais_frete = soma_carrinho + frete
    return f'R$ {soma_carrinho_mais_frete:.2f}'.replace('.', ',')
