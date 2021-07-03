from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..models import *


def cart(request):
    context = {}
    context['items'] = []
    if 'cart' in request.session:
        # print(request.session['cart'])
        try:
            # total price
            totalPrice = 0
            for item_id, qty in request.session['cart'].items():
                item = Item.objects.get(pk=item_id)
                product_images = Image.objects.filter(product=item.product)
                if product_images.count() > 0:
                    img = product_images[0].path
                else:
                    img = None
                
                # add total price
                totalPrice += item.price * int(qty)

                context['items'].append((item, qty, img))
            context['totalPrice'] = totalPrice
        except Item.DoesNotExist:
            context['msg'] = 'cart is none'
    
    # get delivery address
    if 'customer' in request.session:
        customer = Customer.objects.get(pk=request.session['customer'])
        deliveryAddresses = DeliveryAddress.objects.filter(customer=customer)
        if deliveryAddresses and len(deliveryAddresses) > 0:
            context['deliveryAddress'] = deliveryAddresses[len(deliveryAddresses) - 1]
    return render(request=request, template_name='cart.html', context=context)

def deleteItem(request, item_id):
    # print(item_id)
    if str(item_id) in request.session['cart']:
        del request.session['cart'][str(item_id)]
    
    # customer being login
    if 'customer' in request.session:
        customer_id = request.session['customer']
        customer = Customer.objects.get(pk=customer_id)
        cart = Cart.objects.get(customer=customer, is_order=False)
        item=Item.objects.get(pk=item_id)
        CartItem.objects.get(cart=cart, item=item).delete()
    # print('after delete item:' , request.session['cart'])

    request.session.modified = True

    return redirect('mystore:cart')

def addToCart(request):
    # item add to cart
    # item_id = request.GET['item_id']
    item_id = request.POST.get('item_id', False)
    print('id:', item_id)
    # qty = int(request.GET['qty'])
    qty = int(request.POST.get('qty', False))
    print('qty:', qty)
    item = Item.objects.get(pk=int(item_id))
    # print('add cart ' + str(item) + ' ' + str(qty))
    if 'customer' in request.session:
        customer_id = request.session['customer']
        customer = Customer.objects.get(pk=customer_id)
        print('customer: ', customer)
        # get cart
        try:
            cart = Cart.objects.get(customer = customer,is_order=False)
        except Cart.DoesNotExist:
            cart = None
        if cart is None:
            cart = Cart()
            cart.customer = customer
            cart.is_order = False
            cart.save()
        # get cart item
        try:
            cartItem = CartItem.objects.get(cart=cart, item=item)
        except CartItem.DoesNotExist:
            cartItem = CartItem()
            cartItem.cart = cart
            cartItem.item = item
            cartItem.qty = 0

        cartItem.qty += qty
        cartItem.save()  
    # add item to session cart
    if 'cart' in request.session:
        cart = request.session['cart']
    else:
        cart = {}
    
    if item_id not in cart:
        cart[item_id] = 0
    cart[item_id] += qty

    request.session['cart'] = cart

    # cal total price
    totalPrice = 0
    for item_id, qty in request.session['cart'].items():
        item = Item.objects.get(pk=item_id)
        totalPrice += item.price * int(qty)

    return JsonResponse({'msg':'add to cart: ' + item_id + ' : ' + str(qty), 'totalPrice': totalPrice})

def setCart(request):
    customer_id = request.session['customer']
    customer = Customer.objects.get(pk=customer_id)
    try:
        cart = Cart.objects.get(customer = customer,is_order=False)
    except Cart.DoesNotExist:
        cart = None
    # customer added cart while not login
    # print('cart user:' + str(cart))
    # print('cart session ', request.session['cart'])
    if 'cart' in request.session:
        if cart: # delete all cart-item in cart of customer
            CartItem.objects.filter(cart=cart).delete()
        else: # add new cart and add item to cartitem
            cart = Cart()
            cart.customer = customer
            cart.is_order = False
            cart.save()
        # add cart item
        for item_id, qty in request.session['cart'].items():
            item = Item.objects.get(pk=item_id)
            cartItem = CartItem()
            cartItem.cart = cart
            cartItem.item = item
            cartItem.qty = qty
            cartItem.save()
    else: # load cart of customer to session cart
        session_cart = {}
        cartItems = CartItem.objects.filter(cart=cart)
        for cartItem in cartItems:
            session_cart[str(cartItem.item.id)] = cartItem.qty
        request.session['cart'] = session_cart
    # print(request.session['cart'])
    

