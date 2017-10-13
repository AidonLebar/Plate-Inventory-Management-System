from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import InventoryItem, Order, OrderItem

def index(request):
    return render(request, 'inventory/index.html')

def inventoryItemIndex(request):
    inventory_item_list = InventoryItem.objects.order_by('item_name')
    context = {'inventory_item_list': inventory_item_list}
    return render(request, 'inventory/inventoryItemIndex.html', context)

def orderIndex(request):
    order_list = Order.objects.order_by('start_time')
    context = {'order_list': order_list}
    return render(request, 'inventory/orderIndex.html', context)

def inventoryDetail(request, inventory_item_id):
    inventoryItem = get_object_or_404(InventoryItem, pk=inventory_item_id)
    return render(request, 'inventory/inventoryDetail.html', {'inventoryItem': inventoryItem})


def orderDetail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'inventory/orderDetail.html', {'order': order})
