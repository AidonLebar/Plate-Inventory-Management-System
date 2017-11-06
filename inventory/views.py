import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages

from .models import InventoryItem, Order, OrderItem
from .forms import quickOrderForm, addItemForm, orderForm, returnItemForm

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
    return render(request, 'inventory/orderDetail.html', {'order': order, 'form': form, 'returnItemForm': returnItemForm})

def quickOrder(request):
    if request.method == 'POST':
        form = quickOrderForm(request.POST)
        if form.is_valid():
            choices = form.cleaned_data['items']
            o = Order(borrower_name = form.cleaned_data['name'], start_time = timezone.now(), end_time = (timezone.now() + datetime.timedelta(hours = 1)), quick_order = True)
            o.save()
            for i in choices:
                o.orderitem_set.create(item = InventoryItem.objects.filter(item_name = i).first(), quantity_borrowed = 1)
            messages.success(request, 'Quick order successful.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, 'Quick order unsuccessful, please select at least one item.')
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
            i = InventoryItem(item_name = name, total_stock = stock)
            i.save()
            messages.success(request, '%s added successfully.' % name)
            return HttpResponseRedirect('/addItem/')
        else:
            messages.error(request, 'Item was not added. Stock must be greater than 0.')
            return HttpResponseRedirect('/addItem/')

def placeOrder(request):
    form = quickOrderForm()
    orderform = orderForm()
    return render(request, 'inventory/placeOrder.html', {'form':form, 'placeorderform': orderform})

def deleteItem(request):
    if request.method == 'POST':
        inventory_item_id = request.POST['item_id']
        item_name = request.POST['item_name']
        if item_name == 'Bowl' or item_name == 'Plate' or item_name == 'Fork' or item_name == 'Spoon':
            messages.warning(request, "%s is a default item and cannot be deleted." % item_name)
        else:
            inventoryItem = get_object_or_404(InventoryItem, pk=inventory_item_id)
            inventoryItem.delete()
            messages.success(request, '%s was successfully deleted.' % item_name)

    return HttpResponseRedirect('/inventory/')

def deleteOrder(request):
    if request.method == 'POST':
        order_id=request.POST['order_id']
        order = get_object_or_404(Order, pk=order_id)
        order.delete()
        messages.success(request, 'Order was successfully deleted.')

    return HttpResponseRedirect('/orders/')

def orderPlaced(request):
    if request.method == 'POST':
        form = orderForm(request.POST)
        if form.is_valid():
            borrower = form.cleaned_data['borrower_name']
            start = form.cleaned_data['start_time']
            end = form.cleaned_data['end_time']
            if end > start:
                o = Order(borrower_name = borrower, start_time = start, end_time = end)
                o.save()
                messages.success(request, 'Order successfully created.')
                return HttpResponseRedirect('/order/%d' % o.id)
            else:
                messages.error(request, 'Start date must be before end date.')
                return HttpResponseRedirect('/placeOrder/')
        else:
            return HttpResponseRedirect('/orders/')

def returnItem(request):
    if request.method == 'POST':
        form = returnItemForm(request.POST)
        if form.is_valid():
            orderItem_id = request.POST['order_item_id']
            orderItem = get_object_or_404(OrderItem, pk=orderItem_id)
            returned = form.cleaned_data['returned']
            order_id = request.POST['order_id']
            order = get_object_or_404(Order, pk=order_id)
            if returned > orderItem.quantity_borrowed:
                messages.error(request, 'Cannot return more than was borrowed')
                return HttpResponseRedirect('/order/%d/' % order.id)
            else:
                orderItem.quantity_returned = returned
                orderItem.save()
                messages.success(request, 'Return successful.')
                return HttpResponseRedirect('/order/%d/' % order.id)

        else:
            messages.error(request, 'Returned amount must be positive')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def returnAll(request):
    if request.method == 'POST':
        order_id=request.POST['order_id']
        order = get_object_or_404(Order, pk=order_id)
        for item in order.orderitem_set.all():
            item.quantity_returned = item.quantity_borrowed
            item.save()
        messages.success(request, 'All items returned.')
        return HttpResponseRedirect('/order/%d/' % order.id)
