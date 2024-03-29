import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required

from .models import InventoryItem, Order, OrderItem
from .forms import quickOrderForm, addItemForm, orderForm, returnItemForm, addOrderItemForm, editItemForm, editOrderForm, editOrderItemForm

@login_required
def index(request):
    """
    A blank placeholder page. Unused.
    """

    form = quickOrderForm()
    return render(request, 'inventory/index.html', {'form': form})

@login_required
def inventoryItemIndex(request):
    """
    A table of all items in inventory, their total stock and current stock.
    """

    inventory_item_list = InventoryItem.objects.order_by('item_name')
    form = quickOrderForm()
    context = {'inventory_item_list': inventory_item_list, 'form': form}
    return render(request, 'inventory/inventoryItemIndex.html', context)

@login_required
def orderIndex(request):
    """
    A table of all orders, their start time and end time. Split into regular orders and quick orders.
    """

    #sorted chronologically with newest orders first
    order_list = Order.objects.order_by('-start_time')
    form = quickOrderForm()
    context = {'order_list': order_list, 'form': form}
    return render(request, 'inventory/orderIndex.html', context)

@login_required
def inventoryDetail(request, inventory_item_id):
    """
    Detail page for an item. Includes name, current stock, average order size, and orders that have ordered it.
    """

    form = quickOrderForm()
    inventoryItem = get_object_or_404(InventoryItem, pk=inventory_item_id)
    return render(request, 'inventory/inventoryDetail.html', {'inventoryItem': inventoryItem, 'form': form})

@login_required
def orderDetail(request, order_id):
    """
    Detail page of orders, including order information and items ordered in it.
    """

    form = quickOrderForm()
    order = get_object_or_404(Order, pk=order_id)
    inventory_list = InventoryItem.objects.order_by('item_name')
    order_item_form = addOrderItemForm()
    #mutates order list in order detail to only allow the addition of items that are not already in order.
    order_item_form.fields['item_to_add'].queryset = InventoryItem.objects.exclude(
        id__in=[o.item.id for o in order.orderitem_set.all()]
    ).order_by('item_name')
    edit_order_item_form = editOrderItemForm()
    return_item_form = returnItemForm()
    return render(request, 'inventory/orderDetail.html', {'order': order, 'form': form, 'returnItemForm': return_item_form, 'inventory_list': inventory_list, 'addForm': order_item_form, 'editOrderItemForm': edit_order_item_form})

@login_required
def quickOrder(request):
    """
    Quick order side bar parsing and pacing of order.
    """

    if request.method == 'POST':
        form = quickOrderForm(request.POST)
        if form.is_valid():
            choices = form.cleaned_data['items']
            o = Order(borrower_name = form.cleaned_data['name'], start_time = timezone.now(), end_time = (timezone.now() + datetime.timedelta(hours = 1)), quick_order = True)
            o.save()
            for i in choices:
                o.orderitem_set.create(item = i, quantity_borrowed = 1)
            messages.success(request, 'Quick order successful.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, 'Quick order unsuccessful, please select at least one item.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def addItem(request):
    """
    Input page for new information to make a new item.
    """

    form = quickOrderForm()
    additemform = addItemForm()
    return render(request, 'inventory/addItem.html', {'form':form, 'additemform': additemform})

@login_required
def itemAdded(request):
    """
    View to process the new item form and add the item.
    """

    if request.method == 'POST':
        form = addItemForm(request.POST)
        if form.is_valid():
            quick_item = form.cleaned_data['quick_order_item']
            name = form.cleaned_data['item_name']
            stock = form.cleaned_data['stock']
            if name not in [item.item_name for item in InventoryItem.objects.all()]: #ensures a unique name for each item
                i = InventoryItem(item_name = name, total_stock = stock, quick_order_item = quick_item)
                i.save()
                messages.success(request, '%s added successfully.' % name)
                return HttpResponseRedirect('/addItem/')
            else:
                messages.error(request, 'Item with name %s already exists, please use a unique name.' % name)
                return HttpResponseRedirect('/addItem/')
        else:
            messages.error(request, 'Item was not added. Stock must be greater than 0.')
            return HttpResponseRedirect('/addItem/')

@login_required
def placeOrder(request):
    """
    Page to input information for a new order.
    """

    form = quickOrderForm()
    orderform = orderForm()
    return render(request, 'inventory/placeOrder.html', {'form':form, 'placeorderform': orderform})

@login_required
def deleteItem(request):
    """
    Processes item deletion.
    """

    if request.method == 'POST':
        inventory_item_id = request.POST['item_id']
        item_name = request.POST['item_name']
        inventoryItem = get_object_or_404(InventoryItem, pk=inventory_item_id)
        inventoryItem.delete()
        messages.success(request, '%s was successfully deleted.' % item_name)

    return HttpResponseRedirect('/inventory/')

@login_required
def deleteOrder(request):
    """
    Processes order deletion.
    """

    if request.method == 'POST':
        order_id=request.POST['order_id']
        order = get_object_or_404(Order, pk=order_id)
        order.delete()
        messages.success(request, 'Order was successfully deleted.')

    return HttpResponseRedirect('/orders/')

@login_required
def orderPlaced(request):
    """
    Processes order placement form and adds it to database.
    """

    if request.method == 'POST':
        form = orderForm(request.POST)
        if form.is_valid():
            borrower = form.cleaned_data['borrower_name']
            start = form.cleaned_data['start_time']
            end = form.cleaned_data['end_time']
            if end > start: #ensures that start date is before end date
                o = Order(borrower_name = borrower, start_time = start, end_time = end)
                o.save()
                messages.success(request, 'Order successfully created.')
                return HttpResponseRedirect('/order/%d' % o.id)
            else:
                messages.error(request, 'Start date must be before end date.')
                return HttpResponseRedirect('/placeOrder/')
        else:
            messages.error(request, 'Date must be a valid date in format YYYY-MM-DD HH:MM:SS.')
            return HttpResponseRedirect('/placeOrder/')

@login_required
def returnItem(request):
    """
    Processes return for a single order item.
    """

    if request.method == 'POST':
        form = returnItemForm(request.POST)
        if form.is_valid():
            orderItem_id = request.POST['order_item_id']
            orderItem = get_object_or_404(OrderItem, pk=orderItem_id)
            returned = form.cleaned_data['returned']
            order_id = request.POST['order_id']
            order = get_object_or_404(Order, pk=order_id)
            if returned > orderItem.quantity_borrowed: #cannot return nore than was borrowed
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

@login_required
def returnAll(request):
    """
    Processes full order return.
    """

    if request.method == 'POST':
        order_id=request.POST['order_id']
        order = get_object_or_404(Order, pk=order_id)
        for item in order.orderitem_set.all():
            item.quantity_returned = item.quantity_borrowed
            item.save()
        messages.success(request, 'All items returned.')
        return HttpResponseRedirect('/order/%d/' % order.id)

@login_required
def addOrderItem(request):
    """
    Processes new item form and adds item to order.
    """

    if request.method == 'POST':
        form = addOrderItemForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item_to_add']
            order_id = request.POST['order_id']
            order = get_object_or_404(Order, pk=order_id)
            quantity = form.cleaned_data['quantity_to_borrow']
            available = item.total_stock
            oi = OrderItem(item = item, order = order, quantity_borrowed = quantity)
            #checks items in orders that overlap in time to ensure that desired amount is available
            for e in Order.objects.all():
                if not(((e.start_time > oi.order.end_time))or((e.end_time < oi.order.start_time))):
                    for i in e.orderitem_set.all():
                        if i.item.item_name == oi.item.item_name:
                            available -= i.quantity_borrowed
            if quantity <= available:
                oi.save()
                messages.success(request, 'Item added successfully.')
                return HttpResponseRedirect('/order/%d/' % order.id)
            else:
                messages.error(request, "Can't borrow desired quantity, only %d available during that time." %available)
                return HttpResponseRedirect('/order/%d/' % order.id)
        else:
            messages.error(request, 'Amount to borrow must be greater than 0.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def editItem(request):
    """
    Page for editing an item.
    """

    if request.method == 'GET':
        item_id=request.GET['item_id']
        item = get_object_or_404(InventoryItem, pk=item_id)
        form = quickOrderForm()
        edit_item_form = editItemForm()
        edit_item_form.fields['quick_order_item'].initial = item.quick_order_item
        edit_item_form.fields['new_name'].initial = item.item_name
        edit_item_form.fields['new_total_stock'].initial = item.total_stock
        return render(request, 'inventory/editItem.html', {'item': item, 'form':form, 'editForm': edit_item_form})

@login_required
def itemEdited(request):
    """
    Processes edit form and edits item in database.
    """

    if request.method == 'POST':
        form = editItemForm(request.POST)
        if form.is_valid():
            item_id=request.POST['item_id']
            item = get_object_or_404(InventoryItem, pk=item_id)
            item_name = item.item_name
            item.item_name = form.cleaned_data['new_name']
            item.total_stock = form.cleaned_data['new_total_stock']
            item.quick_order_item = form.cleaned_data['quick_order_item']
            item.save()
            messages.success(request, 'Item successfully updated.')
            return HttpResponseRedirect('/inventoryItem/%d/' % item.id)
        else:
            messages.error(request, 'Total Stock must be greater than 0.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def editOrder(request):
    """
    Page for editing and order.
    """

    if request.method == 'GET':
        order_id=request.GET['order_id']
        order = get_object_or_404(Order, pk=order_id)
        form = quickOrderForm()
        edit_order_form = editOrderForm()
        edit_order_form.fields['new_borrower'].initial = order.borrower_name
        edit_order_form.fields['new_start_time'].initial = order.start_time
        edit_order_form.fields['new_end_time'].initial = order.end_time
        return render(request, 'inventory/editOrder.html', {'order': order, 'form':form, 'editForm':edit_order_form})

@login_required
def orderEdited(request):
    """
    Processes a order edit form and edits the order.
    """

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
            messages.error(request, 'Date must be a valid date in format YYYY-MM-DD HH:MM:SS.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def editOrderItem(request):
    """
    Processes the editing of an order item.
    """

    if request.method == 'POST':
        form = editOrderItemForm(request.POST)
        if form.is_valid():
            order_id=request.POST['order_id']
            order = get_object_or_404(Order, pk=order_id)
            order_item_id = request.POST['order_item_id']
            order_item = get_object_or_404(OrderItem, pk=order_item_id)
            new_quantity = form.cleaned_data['quantity']
            order_item.quantity_borrowed = new_quantity
            order_item.save()
            messages.success(request, '%s quantity successfully changed' %order_item.item)
            return HttpResponseRedirect('/order/%d/' % order.id)
        else:
            messages.error(request, 'Quantity must be greater than 0.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def deleteOrderItem(request):
    """
    Processes deletion of order items from an order.
    """

    if request.method == 'POST':
        order_id=request.POST['order_id']
        order = get_object_or_404(Order, pk=order_id)
        order_item_id = request.POST['order_item_id']
        order_item = get_object_or_404(OrderItem, pk=order_item_id)
        order_item.delete()
        messages.success(request, '%s successfully deleted' %order_item.item)
        return HttpResponseRedirect('/order/%d/' % order.id)
