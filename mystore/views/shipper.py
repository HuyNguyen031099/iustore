from django.shortcuts import redirect, render
from django.template import Context, context
from django.db.models import Q
from ..models import *
from ..views import cart

def shipper(request):
    orders = Order.objects.filter(Q(statusNow='Đợi giao') | Q(statusNow='Đang giao')|Q(statusNow='Đã giao'))
    orderDone = Order.objects.filter(statusNow='Đã giao')

    context = {}
    context['orders'] = []
    context['orderDone'] = []
    context['items'] = []

    for order in orders:
        cart_items = CartItem.objects.filter( cart =order.cart)
        order_item = str(cart_items[0].qty) + ' ' + cart_items[0].item.name
        if len(cart_items)-1 > 0:
            order_item += ' và ' +  str(len(cart_items)-1)+' các sản phẩm khác'
        order_item = str(cart_items[0].qty) + ' ' + cart_items[0].item.name
        context['orders'].append((order,order_item))

    for order in orderDone:
        cart_items = CartItem.objects.filter( cart =order.cart)
        order_item = str(cart_items[0].qty) + ' ' + cart_items[0].item.name
        if len(cart_items)-1 > 0:
            order_item += ' và ' +  str(len(cart_items)-1)+' các sản phẩm khác'
        order_item = str(cart_items[0].qty) + ' ' + cart_items[0].item.name
        context['orderDone'].append((order,order_item))


    cart_item = CartItem.objects.filter(cart=order.cart)
    context['items'] = []
    for citem in cart_item:
        amount = citem.qty * citem.item.price
        context['items'].append((citem, amount))

    return render(request, 'manager/shipment.html',context)

def shipping (request,order_id):

    order = Order.objects.get(id = order_id)
    order.statusNow = 'Đang giao'
    print(order)
    
    print(order.statusNow)

    member = Member.objects.get(id = request.session.get('member'))
    print(member)
    updateStatus = OrderHistory()
    updateStatus.member = member
    updateStatus.order = order
    updateStatus.status = order.statusNow
    updateStatus.save()

    # shipper
    shipper = Shipper()
    shipper.member = member
    shipper.save()

    shipment = order.shipment
    shipment.shipper = shipper
    shipment.save()
    
    order.save()
    
    return redirect('mystore:shipper')

def finished (request,order_id):
    
    order = Order.objects.get(id = order_id)
    order.statusNow = 'Đã giao'
    order.save()
    print(order)
    
    print(order.statusNow)

    member = Member.objects.get(id = request.session.get('member'))
    updateStatus = OrderHistory()
    updateStatus.member = member
    updateStatus.order = order
    updateStatus.status = order.statusNow
    updateStatus.save()
    return redirect('mystore:shipper')