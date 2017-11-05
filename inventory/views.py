import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages

from .models import InventoryItem, Order, OrderItem
from .forms import quickOrderForm, addItemForm

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
            o = Order(borrower_name = form.cleaned_data['name'], start_time = timezone.now(), end_time = (timezone.now() + datetime.timedelta(hours = 1)), quick_order = True)
            o.save()
            for i in choices:
                o.orderitem_set.create(item = InventoryItem.objects.filter(item_name = i).first(), quantity_borrowed = 1)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def addItem(request):
    form = quickOrderForm()
    additemform = addItemForm()
    return render(request, 'inventory/addItem.html', {'form':form, 'additemform': additemform})

def itemAdded(request):
    if request.method == 'POST':
        form = addItemForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['item_name']
            stock = form.cleaned_data['stock']
            messages.success(request, '%s added successfully.' % name)
            i = InventoryItem(item_name = name, total_stock = stock)
            i.save()
            return HttpResponseRedirect('/addItem/')
        else:
            messages.error(request, 'Item was not added. Stock must be greater than 0.')
            return HttpResponseRedirect('/addItem/')

def placeOrder(request):
    form = quickOrderForm()
    return render(request, 'inventory/placeOrder.html', {'form':form})

def deleteItem(request):
    if request.method == 'POST':
        inventory_item_id = request.POST['item_id']
        item_name = request.POST['item_name']
        if item_name == 'Bowl' or item_name == 'Plate' or item_name == 'Fork' or item_name == 'Spoon':
            messages.warning(request, "%s should not be deleted for internal reasons." % item_name)
        else:
            inventoryItem = get_object_or_404(InventoryItem, pk=inventory_item_id)
            inventoryItem.delete()
            messages.success(request, '%s was successfully deleted.' % item_name)

    return HttpResponseRedirect('/inventory/')
