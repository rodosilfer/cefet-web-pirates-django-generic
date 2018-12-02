from django.shortcuts import render
from django.db.models import F,ExpressionWrapper,DecimalField
from django.http import HttpResponseRedirect
from django.views import View
from django.forms import ModelForm
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import  ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin 

from .models import Tesouro
# Create your views here.
class ListarTesouros(LoginRequiredMixin,ListView):
   
     model = Tesouro
     template_name = "lista_tesouros.html"
     def get_queryset(self):
        return Tesouro.objects.annotate(valor_total=ExpressionWrapper(F('quantidade')*F('preco'),\
                            output_field=DecimalField(max_digits=10,\
                                                    decimal_places=2,\
                                                     blank=True)\
                                                    )\
                            )
def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        valor_total = 0
        for tesouro in context.get('object_list',[]):
            valor_total += tesouro.valor_total
        context.update({'total_geral': valor_total})
        return context
class TesouroForm(LoginRequiredMixin,ModelForm):
    class Meta:
        model = Tesouro
        fields = ['nome', 'quantidade', 'preco', 'img_tesouro']
        labels = {
            "img_tesouro": "Imagem"
        }

class SalvarTesouro(LoginRequiredMixin,View):
    model = Tesouro
    fields = ['nome', 'quantidade', 'preco', 'img_tesouro']
    template_name = "salvar_tesouro.html"
    success_url = reverse_lazy('lista_tesouros')

class InserirTesouro(SalvarTesouro,CreateView):
    pass

class AtualizarTesouro(SalvarTesouro,UpdateView):
    pass

class RemoverTesouro(DeleteView):
    model = Tesouro
    success_url = reverse_lazy('lista_tesouros')
