from django.shortcuts import render
from django.http import JsonResponse
from ..models import Type, Category

def getTypeByCategory(request):
    category_id = request.GET['category_id']
    category = Category.objects.get(pk=category_id)
    types = Type.objects.filter(category=category)
    res = []

    for t in types:
        res.append((t.id, t.name))
    return JsonResponse({'types': res})

