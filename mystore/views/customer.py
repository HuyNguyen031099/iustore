from ..models import *
from django.shortcuts import render


def notification(request):

    customer = Customer.objects.filter(member = request.session.get('member'))
    listNofi = Notification.objects.filter(customer=customer[0])
    print(listNofi)
    context = {}
    context['listNofi'] = listNofi

    return render(request, 'customer/notification.html',context)


def info(request):
    member = Member.objects.get(id=request.session.get('member'))
    customer = Customer.objects.get(member=member)

    context = {}
    context['customer'] = customer

    return render(request, 'customer/user-info.html',context)


def viewOrderDetail(request, order_id):

    context = {}
    order = Order.objects.get(pk=order_id)

    cart_items = CartItem.objects.filter(cart = order.cart)
    items = []
    totalPrice = 0
    for cart_item in cart_items:
        totalPrice += cart_item.item.price * cart_item.qty
        images = Image.objects.filter(product=cart_item.item.product)
        if images.count() > 0:
            img = images[0].path
        else:
            img = None
        items.append((cart_item.item, cart_item.qty, img,cart_item.item.price*cart_item.qty))

    context['totalPrice'] = totalPrice
    context['items'] = items
    context['order'] = order
    context['totalPriceWithFee'] = order.shipment.shipmentMethod.fee + totalPrice
    return render(request, 'customer/order_detail.html', context)
def order(request):
    context = {}
    context['orders'] = []
    
    member = Member.objects.get(id=request.session.get('member'))
    print(member)
    customer = Customer.objects.get(member=member)

    carts = Cart.objects.filter(customer = customer,is_order='True')
    print(carts)
    
    for cart in carts:
        
        order = Order.objects.get(cart=cart)
        
        cart_items = CartItem.objects.filter( cart = cart)
        order_item = str(cart_items[0].qty) + ' ' + cart_items[0].item.name
        if len(cart_items)-1 > 0:
            order_item += ' và ' +  str(len(cart_items)-1)+' các sản phẩm khác'
        order_item = str(cart_items[0].qty) + ' ' + cart_items[0].item.name
        
        totalPrice = 0
        for cart_item in cart_items:
            totalPrice += cart_item.item.price * cart_item.qty
    
        context['orders'].append((order,order_item, totalPrice))

    return render(request, 'customer/order.html',context)

def address(request):
    context = {}
    customer = Customer.objects.filter(member = request.session.get('member'))
    deliveryAddresses = DeliveryAddress.objects.filter(customer=customer[0])
    if deliveryAddresses and len(deliveryAddresses) > 0:
        context['add'] = deliveryAddresses[len(deliveryAddresses) - 1]
    

    return render(request, 'customer/address.html',context)