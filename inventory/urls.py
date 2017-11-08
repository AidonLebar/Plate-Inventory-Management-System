from django.conf.urls import url

from . import views

app_name = 'inventory'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^inventory/$', views.inventoryItemIndex, name='inventoryItemIndex'),
    url(r'^orders/$', views.orderIndex, name='orderIndex'),
    url(r'^inventoryItem/(?P<inventory_item_id>[0-9]+)/$', views.inventoryDetail, name='inventoryDetail'),
    url(r'^order/(?P<order_id>[0-9]+)/$', views.orderDetail, name='orderDetail'),
    url(r'^quickOrder/$', views.quickOrder, name='quickOrder'),
    url(r'^addItem/$', views.addItem, name='addItem'),
    url(r'^itemAdded/$', views.itemAdded, name='itemAdded'),
    url(r'^placeOrder/$', views.placeOrder, name='placeOrder'),
    url(r'^deleteItem/$', views.deleteItem, name='deleteItem'),
    url(r'^deleteOrder/$', views.deleteOrder, name='deleteOrder'),
    url(r'^orderPlaced/$', views.orderPlaced, name='orderPlaced'),
    url(r'^returnItem/$', views.returnItem, name='returnItem'),
    url(r'^returnAll/$', views.returnAll, name='returnAll'),
    url(r'^addOrderItem/$', views.addOrderItem, name='addOrderItem'),
    url(r'^editItem/$', views.editItem, name='editItem'),
    url(r'^itemEdited/$', views.itemEdited, name='itemEdited'),
    url(r'^editOrder/$', views.editOrder, name='editOrder'),
    url(r'^orderEdited/$', views.orderEdited, name='orderEdited'),
    url(r'^editOrderItem/$', views.editOrderItem, name='editOrderItem'),
]
