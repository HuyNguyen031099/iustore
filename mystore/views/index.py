from django.shortcuts import render
from django.template import Context, context
from ..models import *


def home(request):
    items = Item.objects.all()
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
            discount_rate = round(discount.discount_value / item.price * 100) - 100
        except Discount.DoesNotExist:
            pass
        
        context['items'].append((item,img, discount_rate))
    print(context['items'])
    return render(request, 'home.html',context)