from django.shortcuts import render
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
