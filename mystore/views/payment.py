from django.shortcuts import render, redirect
from ..views import addressAPI
from ..models import *

def checkout(request):
    if 'user' not in request.session:
        return redirect('mystore:login')
    
    context = {}

    shipmentMethods = ShipmentMethod.objects.all()
    context['shipmentMethods'] = shipmentMethods

    paymentMethods = PaymentMethod.objects.all()
    context['paymentMethods'] = paymentMethods

    banks = Bank.objects.all()
    context['banks'] = banks

    context['items'] = []
    if 'cart' in request.session:
        # print(request.session['cart'])
        try:
            # total price
            totalPrice = 0
            for item_id, qty in request.session['cart'].items():
                item = Item.objects.get(pk=item_id)
                product_images = Image.objects.filter(product=item.product)
                img_path = product_images[0].path
                # add total price
                totalPrice += item.price * int(qty)

                context['items'].append((item, qty, img_path))
            context['totalPrice'] = totalPrice
        except Item.DoesNotExist:
            context['msg'] = 'cart is none'
    
    # get delivery address
    if 'customer' in request.session:
        customer = Customer.objects.get(pk=request.session['customer'])
        deliveryAddresses = DeliveryAddress.objects.filter(customer=customer)
        if deliveryAddresses and len(deliveryAddresses) > 0:
            context['deliveryAddress'] = deliveryAddresses[len(deliveryAddresses) - 1]

    return render(request, 'checkout/checkout.html', context)

def handleCheckout(request):

    shipment_method_id = request.POST['shipment_method']
    payment_method_name = request.POST['payment_method']

    # get customer
    customer_id = request.session['customer']
    customer = Customer.objects.get(pk=customer_id)
    cart = Cart.objects.get(customer=customer,is_order=False)
    deliveryAddresses = DeliveryAddress.objects.filter(customer=customer)

    # shipment
    shipment = Shipment()
    shipmentMethod = ShipmentMethod.objects.get(pk=shipment_method_id)
    shipment.shipmentMethod = shipmentMethod
    
    
    # payment
    payment = Payment()
    paymentMethod = PaymentMethod.objects.get(method_name=payment_method_name)        
    payment.paymentmethod = paymentMethod
    if payment_method_name == 'Thẻ ATM': # ATM payment method
        # payment detail
        paymentDetail = PaymentDetail()
        bank = Bank.objects.get(pk=request.POST['bank'])
        paymentDetail.customer = request.POST['customer_name']
        paymentDetail.bank = bank
        paymentDetail.card = request.POST['card_code']
        paymentDetail.save()
        payment.paymentDetail = paymentDetail
    
    shipment.save()
    payment.save()

    # reset cart
    cart.is_order = True
    if 'cart' in request.session:
        del request.session['cart']
    cart.save()

    # order
    order = Order()
    order.cart = cart
    order.shipment = shipment
    order.payment = payment
    order.deliveryAddress = deliveryAddresses[len(deliveryAddresses) - 1]
    order.statusNow = 'Chờ duyệt'
    order.save() # save order 

    return redirect('mystore:home')

def editDeliveryAddress(request):
    if 'customer' not in request.session:
        return redirect('mystore:login')
    context = {}
    # customer logged
    customer = Customer.objects.get(pk=request.session['customer'])
    deliveryAddresses = DeliveryAddress.objects.filter(customer=customer)
    if deliveryAddresses and len(deliveryAddresses) > 0:
        context['address'] = deliveryAddresses[len(deliveryAddresses) - 1]
    
    cities = addressAPI.getCities()
    context['cities'] = cities 
    return render(request, template_name='checkout/edit-delivery_address.html', context=context)

def handleDeliveryAddress(request):

    name = request.POST['name']
    phone = request.POST['phone']

    customer_id = request.session['customer']
    customer = Customer.objects.get(pk=customer_id)

    address = Address()
    address.city = request.POST['city'].split(',')[1]
    address.district = request.POST['district'].split(',')[1]
    address.ward = request.POST['ward'].split(',')[1]
    address.address = request.POST['address']
    address.save() # save address

    deliveryAddress = DeliveryAddress()
    deliveryAddress.customer = customer
    deliveryAddress.address = address
    deliveryAddress.receiver = name
    deliveryAddress.phone = phone
    deliveryAddress.save() # save delivery address

    return redirect('mystore:delivery-address/show-edit')

def showOrder(request):

    context = {}

    shipmentMethods = ShipmentMethod.objects.all()
    context['shipmentMethods'] = shipmentMethods

    paymentMethods = PaymentMethod.objects.all()
    context['paymentMetods'] = paymentMethods


