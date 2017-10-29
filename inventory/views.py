import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from .models import InventoryItem, Order, OrderItem
from .forms import quickOrderForm

def index(request):
    form = quickOrderForm()
    return render(request, 'inventory/index.html', {'form': form})

def inventoryItemIndex(request):
    inventory_item_list = InventoryItem.objects.order_by('item_name')
    form = quickOrderForm()
    context = {'inventory_item_list': inventory_item_list, 'form': form}
    return render(request, 'inventory/inventoryItemIndex.html', context)

def orderIndex(request):
    order_list = Order.objects.order_by('start_time')
    form = quickOrderForm()
    context = {'order_list': order_list, 'form': form}
    return render(request, 'inventory/orderIndex.html', context)

def inventoryDetail(request, inventory_item_id):
    form = quickOrderForm()
    inventoryItem = get_object_or_404(InventoryItem, pk=inventory_item_id)
    return render(request, 'inventory/inventoryDetail.html', {'inventoryItem': inventoryItem, 'form': form})

def orderDetail(request, order_id):
    form = quickOrderForm()
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'inventory/orderDetail.html', {'order': order, 'form': form})

def quickOrder(request):
    if request.method == 'POST':
        form = quickOrderForm(request.POST)
        if form.is_valid():
            choices = form.cleaned_data['items']
            o = Order(borrower_name = form.cleaned_data['name'], start_time = timezone.now(), end_time = (timezone.now() + datetime.timedelta(hours = 2)))
            o.save()
            for i in choices:
                x = OrderItem(item = InventoryItem.objects.filter(item_name = i).first(), order = o, quantity_borrowed = 1)
                x.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
