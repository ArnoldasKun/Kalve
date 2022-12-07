from django.core.paginator import Paginator
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
    paginator = Paginator(Blacksmith.objects.all(), 5)
    page_number = request.GET.get('page')
    paged_blacksmiths = paginator.get_page(page_number)
    return render(
        request, 'forge/blacksmiths.html', 
        {'blacksmiths': paged_blacksmiths })

def blacksmith(request, blacksmith_id):
    return render(request, 'forge/blacksmith.html', 
    {'blacksmith': get_object_or_404(Blacksmith, id=blacksmith_id)})


class ArmorListView(ListView):
    model = Armor
    template_name = 'forge/armor_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        armor_type_id = self.request.GET.get('armor_type_id')
        if armor_type_id:
            queryset = queryset.filter(armor_type__id=armor_type_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['armors_count'] = self.get_queryset().count()
        armor_type_id = self.request.GET.get('armor_type_id')
        context['armor_types'] = ArmorType.objects.all()
        if armor_type_id:
            context['armor_type'] = get_object_or_404(ArmorType, id=armor_type_id)
        return context

    
class ArmorDetailView(DetailView):
    model = Armor
    template_name = 'forge/armor_detail.html'
