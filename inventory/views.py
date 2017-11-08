import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages

from .models import InventoryItem, Order, OrderItem
from .forms import quickOrderForm, addItemForm, orderForm, returnItemForm, addOrderItemForm, editItemForm, editOrderForm, editOrderItemForm

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

from django import forms

def orderDetail(request, order_id):
    form = quickOrderForm()
    order = get_object_or_404(Order, pk=order_id)
    inventory_list = InventoryItem.objects.order_by('item_name')
    order_item_form = addOrderItemForm()
    order_item_form.fields['item_to_add'].queryset = InventoryItem.objects.exclude(
        id__in=[o.item.id for o in order.orderitem_set.all()]
    )
    edit_order_item_form = editOrderItemForm()
    return render(request, 'inventory/orderDetail.html', {'order': order, 'form': form, 'returnItemForm': returnItemForm, 'inventory_list': inventory_list, 'addForm': order_item_form, 'editOrderItemForm': edit_order_item_form})

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

def addOrderItem(request):
    if request.method == 'POST':
        form = addOrderItemForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item_to_add']
            order_id = request.POST['order_id']
            order = get_object_or_404(Order, pk=order_id)
            quantity = form.cleaned_data['quantity_to_borrow']
            available = item.total_stock
            oi = OrderItem(item = item, order = order, quantity_borrowed = quantity)
            for e in Order.objects.all():
                if not(((e.start_time > oi.order.end_time))or((e.end_time < oi.order.start_time))):
                    for i in e.orderitem_set.all():
                        if i.item.item_name == oi.item.item_name:
                            available -= i.quantity_borrowed
            if quantity < available:
                oi.save()
                messages.success(request, 'Item added successfully.')
                return HttpResponseRedirect('/order/%d/' % order.id)
            else:
                messages.error(request, "Can't borrow desired quantity, only %d available during that time." %available)
                return HttpResponseRedirect('/order/%d/' % order.id)
        else:
            messages.error(request, 'Amount to borrow must be greater than 0.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def editItem(request):
  if request.method == 'GET':
    item_id=request.GET['item_id']
    item = get_object_or_404(InventoryItem, pk=item_id)
    form = quickOrderForm()
    edit_item_form = editItemForm()
    edit_item_form.fields['new_name'].initial = item.item_name
    edit_item_form.fields['new_total_stock'].initial = item.total_stock
    return render(request, 'inventory/editItem.html', {'item': item, 'form':form, 'editForm': edit_item_form})

def itemEdited(request):
    if request.method == 'POST':
        form = editItemForm(request.POST)
        if form.is_valid():
            item_id=request.POST['item_id']
            item = get_object_or_404(InventoryItem, pk=item_id)
            item_name = item.item_name
            if (item_name == 'Bowl' or item_name == 'Plate' or item_name == 'Fork' or item_name == 'Spoon') and item_name != form.cleaned_data['new_name']:
                messages.warning(request, "%s is a default item and the name cannot be edited." % item_name)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            else:
                item.item_name = form.cleaned_data['new_name']
                item.total_stock = form.cleaned_data['new_total_stock']
                item.save()
                messages.success(request, 'Item successfully updated.')
                return HttpResponseRedirect('/inventoryItem/%d/' % item.id)
        else:
            messages.error(request, 'Total Stock must be greater than 0.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def editOrder(request):
    if request.method == 'GET':
        order_id=request.GET['order_id']
        order = get_object_or_404(Order, pk=order_id)
        form = quickOrderForm()
        edit_order_form = editOrderForm()
        edit_order_form.fields['new_borrower'].initial = order.borrower_name
        edit_order_form.fields['new_start_time'].initial = order.start_time
        edit_order_form.fields['new_end_time'].initial = order.end_time
        return render(request, 'inventory/editOrder.html', {'order': order, 'form':form, 'editForm':edit_order_form})

def orderEdited(request):
    if request.method == 'POST':
        form = editOrderForm(request.POST)
        if form.is_valid():
            order_id = request.POST['order_id']
            order = get_object_or_404(Order, pk=order_id)
            order.borrower_name = form.cleaned_data['new_borrower']
            order.start_time = form.cleaned_data['new_start_time']
            order.end_time = form.cleaned_data['new_end_time']
            order.save()
            messages.success(request, 'Order successfully updated.')
            return HttpResponseRedirect('/order/%d/' % order.id)
        else:
            messages.error(request, 'Date must be in format YYYY-MM-DD HH:MM:SS.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def editOrderItem(request):
    if request.method == 'POST':
        form = editOrderItemForm(request.POST)
        if form.is_valid():
            order_id=request.POST['order_id']
            order = get_object_or_404(Order, pk=order_id)
            order_item_id = request.POST['order_item_id']
            order_item = get_object_or_404(OrderItem, pk=order_item_id)
            new_quantity = form.cleaned_data['quantity']
            if new_quantity == 0:
                order_item.delete()
                messages.success(request, 'Item deleted because quantity borrowed is 0.')
                return HttpResponseRedirect('/order/%d/' % order.id)
            else:
                order_item.quantity_borrowed = new_quantity
                order_item.save()
                messages.success(request, '%s quantity successfully changed' %order_item.item)
                return HttpResponseRedirect('/order/%d/' % order.id)
        else:
            messages.error(request, 'Quantity must be 0(if you wish to delete item) or greater.')
            return HttpResponseRedirect('/order/%d/' % order.id)
