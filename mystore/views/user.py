from django.shortcuts import redirect, render
from django.template import Context, context
from ..models import *
from ..views import cart

def login(request):

    if request.method == 'GET':
        if 'user' in request.session:
            return redirect('mystore:home')

        return render(request, 'user/login.html')

    if request.method == 'POST':
        usn = request.POST.get('username')
        pwd = request.POST.get('password')
        try:
            user = Account.objects.get(username=usn)
        except Account.DoesNotExist:
            message = "User not exist, please login!!"
            return render(request, 'user/login.html', {"msg_user": message})
        if user.password != pwd:
            message = "Wrong password!!"
            return render(request, 'user/login.html', {"msg_user": message})

        member = Member.objects.get(account=user)
        request.session['user'] = member.name   
        request.session['member'] = member.id

        # customer
        if user.permission.level == 3:
            # set cart for customer
            customer = Customer.objects.get(member=member)
            request.session['customer'] = customer.id
            cart.setCart(request)
            return redirect('mystore:home')
        else:
            return redirect('mystore:saler')


def logout(request):
    if 'user' in request.session:
        del request.session['user']
    if 'customer' in request.session:
        del request.session['customer']
    if 'member' in request.session:
        del request.session['member']
    if 'cart' in request.session:
        del request.session['cart']
    return redirect('mystore:home')


def register(request):
    if request.POST:
        return doRegister(request)
    return render(request, 'user/register.html')

def doRegister(request):
    context = {}
    if request.POST:
        usr = request.POST.get('usr')
        pwd = request.POST.get('password')

        name = request.POST.get('name')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        phone = request.POST.get('phone')

        city = request.POST.get('city')
        district = request.POST.get('district')
        ward = request.POST.get('ward')
        description = request.POST.get('addr')
        addres = Address(city=city, district=district, ward=ward, address=description)

        selected = request.POST.get('gender')
        gender = -1
        if selected == 'Male':
            gender = 0
        else: 
            gender = 1

        account = Account.objects.filter(username=usr)
        if account:
            context['mess'] = "Người dùng đã tồn tại, hãy đăng nhập"
            return render(request, 'user/login.html')
        else:
            addres.save()

            permission = Permission(level=3, description='customer')
            permission.save()

            acc = Account(username=usr, password=pwd, permission=permission)
            acc.save()

            user = Member(name=name, email=email, phone=phone, dob=dob, gender=gender, avatar=None, address=addres, account=acc)
            user.save()

            customer = Customer(member=user)
            customer.save()

            context['username'] = acc.username
            context['password'] = acc.password
            return render(request, 'user/login.html', context)