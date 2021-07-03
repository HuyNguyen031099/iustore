from django.shortcuts import render, redirect
from ..models import *

def saler(request):
    orders = Order.objects.all()
    context = {}
    context['orders'] = []
    for order in orders:
        cart_items = CartItem.objects.filter( cart =order.cart)
        order_item = str(cart_items[0].qty) + ' ' + cart_items[0].item.name
        if len(cart_items)-1 > 0:
            order_item += ' và ' +  str(len(cart_items)-1)+' các sản phẩm khác'
        order_item = str(cart_items[0].qty) + ' ' + cart_items[0].item.name
        context['orders'].append((order,order_item))
    return render(request, 'manager/saler.html',context)

def shipment(request):
    return render(request, 'manager/shipment.html')

def newProduct(request):
    categories = Category.objects.all()
    context = {}
    context['categories'] = []
    for category in categories:
        context['categories'].append(category)
    return render(request, template_name='manager/new-product.html', context=context)

def newProductDetail(request, type_id):
    context = {}
    context['type_id'] = type_id
    typee = Type.objects.get(pk=type_id)
    # attributes of product type
    typeAttributes = AttributeType.objects.filter(type=typee)
    
    context['attributes'] = typeAttributes
    print(typeAttributes)
    # all warehouses
    warehouses = Warehouse.objects.all()
    context['warehouses'] = warehouses
    return render(request, template_name='manager/new-product-detail.html', context=context)

def importProduct(request):
    
    images = []

    for f in request.FILES.getlist('image'):
        images.append(f.name)
    
    warehouse_id = request.POST['warehouse']
    product_name = request.POST['product-name']
    product_price = (float)(request.POST['price'])
    description = request.POST['description']
    quantity = int(request.POST['qty'])
    type_id = request.POST['type_id']

    # save product
    product = Product()
    product.warehouse = Warehouse.objects.get(pk=warehouse_id)
    product.name = product_name
    product.price = product_price
    product.qty_in_stock = quantity
    product.type = Type.objects.get(pk=type_id)
    
    product.save()
    
    # save images
    for img_name in images:
        image = Image()
        image.product = product
        image.path = img_name
        image.save()
    # save import file
    importFile = ImportFile()
    importFile.save()

    # save import product
    importProduct = ImportProduct()
    importProduct.product = product
    importProduct.import_file = importFile
    importProduct.qty = quantity
    importProduct.save()

    attributes = AttributeType.objects.filter(type = Type.objects.get(pk=type_id))
    for attributeType in attributes:
        att_value = AttributeValue()
        att_value.product = product
        att_value.attribute = attributeType.attribute
        att_value.value = request.POST[str(attributeType.attribute.id)]
        # save product attribute value
        att_value.save()
    
    return redirect("mystore:new-product")

def sendWarehouse(request,order_id):

    order = Order.objects.get(id = order_id)
    order.statusNow = 'Đợi kho'
    order.save()

    member = Member.objects.get(id = request.session.get('member'))
    updateStatus = OrderHistory(order=order,status=order.statusNow,member=member)
    updateStatus.save()

    # Thông báo cho khách hàng
    notification = Notification()
    notification.customer = order.cart.customer
    notification.content = 'Đơn hàng mã ' + str(order.id) + ' đã được chúng tôi tiếp nhận'
    notification.attach = 'saler/view-order/'+str(order.id)
    notification.save()


    return redirect('mystore:saler')
    
def viewOrder(request,order_id):
    context = {}
    order = Order.objects.get(id=order_id)
    cart_item = CartItem.objects.filter(cart=order.cart)
    
    sum = 0
    context['items'] = []
    for citem in cart_item:
        amount = citem.qty * citem.item.price
        sum += amount
        context['items'].append((citem, amount))
    
    customer = Member.objects.get(id=order.cart.customer.member.id)

    shipment = Shipment.objects.get(id=order.shipment.id)
    # shipper = Member.objects.get(id=shipment.shipper.member.id)
    tax = int(0.05 * sum)
    total = sum + tax
    context['order'] = order
    context['customer'] = customer
    context['citem'] = cart_item
    # context['shipper'] = shipper
    context['subtotal'] = sum
    context['tax'] = tax
    context['total'] = total
    return render(request, 'manager/view-order.html', context)