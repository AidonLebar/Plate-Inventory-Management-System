from django.conf.urls import url

from . import views

app_name = 'inventory'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^inventory/$', views.inventoryItemIndex, name='inventoryItemIndex'),
    url(r'^orders/$', views.orderIndex, name='orderIndex'),
    url(r'^inventoryItem/(?P<inventory_item_id>[0-9]+)/$', views.inventoryDetail, name='inventoryDetail'),
    url(r'^order/(?P<order_id>[0-9]+)/$', views.orderDetail, name='orderDetail')
]
