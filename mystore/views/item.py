from os import name
from ..views.product import product
from django.shortcuts import render, redirect
from ..models import *


def showItemDetail(request, item_id):

    context = {}
    item = Item.objects.get(pk=item_id)
    product = item.product
    product_images = Image.objects.filter(product=product)
    if product_images.count() > 0:
        img = product_images[0].path
    else:
        img = None
    context['img_path'] = img

    discount_rate = None
    discout_price = None
    try:
        discount = Discount.objects.get(id=item.id)
        discout_price = discount.discount_value
        discount_rate = round(discount.discount_value / item.price * 100) - 100
    except Discount.DoesNotExist:
        pass

    current_price = item.price

    attribute_values = AttributeValue.objects.filter(product=item.product)
    attrs = []
    attr_values = []
    for i in attribute_values:
        attrs.append(Attribute.objects.get(id=i.attribute.id))
        attr_values.append(i.value)

    # feedback
    fbs = []
    feedbacks = Feedback.objects.filter(item=item)
    for feedback in feedbacks:
        rate = [1 for _ in range(feedback.rate_score)]
        fbs.append((feedback, rate))

    context['item'] = item
    context['product'] = item.product
    context['current_price'] = current_price
    context['discount_price'] = discout_price
    context['discount_rate'] = discount_rate
    context['attrs'] = attrs
    context['attribute_values'] = attr_values

    context['feedBacks'] = fbs[::-1]

    # similar items
    context['items'] = []
    items = getSimilarItem(item_id)
    for item in items:
        product = item.product
        product_images = Image.objects.filter(product=product)
        if product_images.count() > 0:
            img = product_images[0].path
        else:
            img = None
        discount_rate = None
        try:
            discount = Discount.objects.get(id=item.id)
            discount_rate = round(
                discount.discount_value / item.price * 100) - 100
        except Discount.DoesNotExist:
            pass

        context['items'].append((item, img, discount_rate))
    return render(request, "item_detail.html", context)


def searchItem(request):

    query = request.GET['q']
    items = Item.objects.filter(name__icontains=query)

    context = {}
    context['items'] = []
    for item in items:
        product = item.product
        product_images = Image.objects.filter(product=product)
        if product_images.count() > 0:
            img = product_images[0].path
        else:
            img = None
        discount_rate = None
        try:
            discount = Discount.objects.get(id=item.id)
            discount_rate = round(
                discount.discount_value / item.price * 100) - 100
        except Discount.DoesNotExist:
            pass

        context['items'].append((item, img, discount_rate))
    context['query'] = query

    return render(request, 'search_item.html', context)


def showItemComment(request, item_id):
    context = {}
    item = Item.objects.get(pk=item_id)
    product = item.product
    product_images = Image.objects.filter(product=product)
    if product_images.count() > 0:
        img = product_images[0].path
    else:
        img = None
    context['img_path'] = img

    discount_rate = None
    discout_price = None
    try:
        discount = Discount.objects.get(id=item.id)
        discout_price = discount.discount_value
        discount_rate = round(discount.discount_value / item.price * 100) - 100
    except Discount.DoesNotExist:
        pass

    current_price = item.price

    attribute_values = AttributeValue.objects.filter(product=item.product)
    attrs = []
    attr_values = []
    for i in attribute_values:
        attrs.append(Attribute.objects.get(id=i.attribute.id))
        attr_values.append(i.value)

    # feedback
    fbs = []
    feedbacks = Feedback.objects.filter(item=item)
    for feedback in feedbacks:
        rate = [1 for _ in range(feedback.rate_score)]
        fbs.append((feedback, rate))

    context['item'] = item
    context['product'] = item.product
    context['current_price'] = current_price
    context['discount_price'] = discout_price
    context['discount_rate'] = discount_rate
    context['attrs'] = attrs
    context['attribute_values'] = attr_values
    context['feedBacks'] = fbs[::-1]
    context['comment'] = True
    return render(request, "item_detail.html", context)


def handleComment(request):
    rate = request.POST['rate']
    item_id = request.POST['item_id']

    # customer
    customer_id = request.session['customer']
    customer = Customer.objects.get(pk=customer_id)

    # comment
    comment = Comment()
    comment.content = request.POST['customer-comment']
    comment.save()

    feedBack = Feedback()
    feedBack.customer = customer
    feedBack.item = Item.objects.get(pk=item_id)
    feedBack.rate_score = rate
    feedBack.comment = comment
    feedBack.save()

    return showItemDetail(request, item_id)


def getSimilarItem(item_id):

    item = Item.objects.get(pk=item_id)

    typee = Type.objects.get(pk=item.product.type.id)

    products = Product.objects.filter(type=typee)

    items = []
    for product in products:
        try:
            itemm = Item.objects.get(product=product)
            items.append(itemm)
        except Item.DoesNotExist:
            pass
    return [it for it in items if it.id != item.id]


def item_type(request, type_id):
    type = Type.objects.get(id = type_id )
    products = Product.objects.filter(type = type)
    
    items = []
    for product in products:
        try:
            itemm = Item.objects.get(product=product)
            items.append(itemm)
        except Item.DoesNotExist:
            pass
    

    context = {}
    context['items'] = []
    for item in items:
        product = item.product
        product_images = Image.objects.filter(product=product)
        if product_images.count() > 0:
            img = product_images[0].path
        else:
            img = None
        discount_rate = None
        try:
            discount = Discount.objects.get(id=item.id)
            discount_rate = round(
                discount.discount_value / item.price * 100) - 100
        except Discount.DoesNotExist:
            pass

        context['items'].append((item, img, discount_rate))
    context['type'] = type

    return render(request, 'search_item.html', context)