from django.shortcuts import redirect, render
from django.template import Context, context
from ..models import *

def product(request):

    products = Product.objects.all()
    context = {}
    context['products'] = products
    return render(request, 'manager/product.html',context)

def active(request):
    items = Item.objects.all()
    products =[]
    for item in items:
        products.append(item.product)
    context = {}
    context['products'] = products
    context['msg'] = 'active'
    return render(request, 'manager/product.html',context)

def checkExist(product, items):
    for item in items:
        if item.product.id == product.id:
            return False
    return True
def getList(request):
    context = {}
    items = Item.objects.all()
    products = Product.objects.all()

    prs = []
    for product in products:
        if checkExist(product, items):
            prs.append(product)
    
    context['up'] = prs
    return render(request, 'manager/up-shelf.html', context)

def showUpShelfForm(request, product_id):
    # print(product_id)
    product = Product.objects.get(id=product_id)
    context = {}
    context['product'] = product
    return render(request, 'manager/up-shelf-detail.html', context)

def upShelf(request):
    product_name = request.POST.get('name')
    product = Product.objects.get(name=product_name)

    if request.POST:
        price = request.POST.get('price-sale')
        discount = request.POST.get('discount')
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        
        # save item
        item = Item(product=product, name=product.name, price=price)
        item.save()

        # save discount
        disc = Discount(item=item, discount_value=discount, from_date=fromdate, to_date=todate)
        disc.save()
    return redirect('mystore:product')

def showEditProductForm(request, product_id):
    context = {}
    context['attributes'] = []

    product = Product.objects.get(pk=product_id)

    attribute_values = AttributeValue.objects.filter(product=product)
    for i in attribute_values:
        context['attributes'].append((Attribute.objects.get(id=i.attribute.id), i.value))

    warehouses = Warehouse.objects.all()
    # print(context['attributes'])
    context['product'] = product
    context['warehouses'] = warehouses

    return render(request, 'manager/edit-product.html', context)

def editProduct(request, product_id):
    p = Product.objects.get(pk=product_id)
    if request.POST:    
        name = request.POST.get('product-name')
        price = request.POST.get('price')
        qty = request.POST.get('qty')

        Product.objects.filter(pk=product_id).update(name=name, price=price, qty_in_stock=qty, type=p.type)
    return redirect('mystore:product')

def deleteProduct(request, product_id):
    p = Product.objects.get(pk=product_id)
    image = Image.objects.get(product=p)
    attr_values = AttributeValue.objects.filter(product=p)
    print(attr_values)
    attr_values.delete()
    image.delete()
    p.delete()
    return redirect('mystore:product')