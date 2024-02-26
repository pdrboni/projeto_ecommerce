import requests
import pprint

url = "https://www.melhorenvio.com.br/api/v2/me/shipment/calculate"

payload = {
    "from": { "postal_code": "90010313" },
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

response = requests.post(url, json=payload, headers=headers)

pprint.pprint(response.json())

        perfil = Perfil.objects.filter(usuario=self.request.user)
    
        for p in perfil:
            url = "https://www.melhorenvio.com.br/api/v2/me/shipment/calculate"

            payload = {
                "from": { "postal_code": f"{p.cep}" },
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

            '''print(retorno[1]['name'])
            print(retorno[1]['price'])
            print(retorno[2]['name'])
            print(retorno[2]['price'])'''

            contexto = {
                'usuario': self.request.user,
                'carrinho': self.request.session['carrinho'],
                'cep' : retorno,
                'transp1' : retorno[1]['name'],
                'valor1' : float(retorno[1]['price']),
                'transp2' : retorno[2]['name'],
                'valor2' : float(retorno[2]['price'])
            }

        return render(self.request, 'produto/resumodacompra.html', contexto)


lista = [{id : 1, price: 3.90, weight: 1.2}, {id : 2, weight: 1.4}, {id : 3, price: 4.90}, {id : 4, price: 5.90, weight: 2.2}, {id : 5, weight: 1.0}]