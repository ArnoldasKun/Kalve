from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from . models import Blacksmith, Armor, ArmorType, ArmorOrder

# Create your views here.

def index(request):
    armor_count = Armor.objects.count()
    armor_order_count = ArmorOrder.objects.count()
    blacksmith_count = Blacksmith.objects.count()

    context = {
        'armor_count': armor_count,
        'armor_order_count': armor_order_count,
        'blacksmith_count': blacksmith_count,
        'armor_type_count': ArmorType.objects.count()
    }

    return render(request, 'forge/index.html', context)

def blacksmiths(request):
    return render(
        request, 'forge/blacksmiths.html', 
        {'authors': Blacksmith.objects.all()})

def blacksmith(request, blacksmith_id):
    return render(request, 'forge/blacksmith.html', 
    {'blacksmith': get_object_or_404(Blacksmith, id=blacksmith_id)})


class ArmorListView(ListView):
    model = Armor
    template_name = 'forge/armor_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['armors_count'] = self.get_queryset().count()
        return context


class ArmorDetailView(DetailView):
    model = Armor
    template_name = 'forge/armor_detail.html'
