from django.shortcuts import render
from django.http import JsonResponse
from ..models import Bank

def getBanks(request):
    banks = Bank.objects.all()
    res = []
    for bank in banks:
        res.append((bank.id, bank.name,bank.logo))
    return JsonResponse(res, safe=False)