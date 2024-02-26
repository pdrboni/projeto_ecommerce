from django.urls import path
from . import views

app_name = 'cupom'

urlpatterns = [
    path('cupom/', views.AssimilaCupom.as_view(), name='cupom'),
    path('removercupom/', views.RemoverCupom.as_view(), name='removercupom'),
]
