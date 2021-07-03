from django.shortcuts import render
from django.http import JsonResponse
import json
import requests

def getCities():    
    url = 'https://thongtindoanhnghiep.co/api/city'
    r = requests.get(url)
    if r.status_code == 200:
        city_json = r.json()
        cities = [(item['ID'], item['Title']) for item in city_json['LtsItem']]
        return cities
    return []

def getDistrictsInCity(request, city_id):
    url = 'https://thongtindoanhnghiep.co/api/city/'+str(city_id)+'/district'
    r = requests.get(url)
    if r.status_code == 200:
        districts = [(item['ID'],item['Title']) for item in r.json()]
        return JsonResponse(districts, safe=False)
    return JsonResponse({})
def getWardsInDistrict(request, district_id):
    url = 'https://thongtindoanhnghiep.co/api/district/'+str(district_id)+'/ward'
    r = requests.get(url)
    if r.status_code == 200:
        wards = [(item['ID'],item['Title']) for item in r.json()]
        return JsonResponse(wards, safe=False)
    return JsonResponse({})