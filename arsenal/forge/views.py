from django.shortcuts import render
from . models import Blacksmith, Armor, ArmorType, ArmorOrder

# Create your views here.

def index(request):
    armor_count = Armor.objects.count()
    armor_order_count = ArmorOrder.objects.count()
    blacksmith_count = Blacksmith.objects.count()

    context = {
        'book_count': armor_count,
        'book_instance_count': armor_order_count,
        'blacksmith_count': blacksmith_count,
        'genre_count': ArmorType.objects.count()
    }

    return render(request, 'library/index.html', context)
