from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control
from django.http import JsonResponse
import json
import datetime
import requests
from .models import *

# Create your views here.

def mobile(request):
    if request.method=='POST':
        number = request.POST['number']
        user=User.objects.get(last_name=number)
        print(user)

        if user:
            username = user.username
            password=user.first_name
            request.session['username'] =  username
            request.session['password'] = password
            

            url = "https://d7networks.com/api/verifier/send"
            number=str(91) + number
            
            payload = {'mobile': number,
            'sender_id': 'SMSINFO',
            'message': 'Your otp code is {code}',
            'expiry': '900'}
            files = [

            ]
            headers = {
            'Authorization': 'Token 0d21f1e3cb977b24ebd925ec71d3fec0cb0a41f3'
            }

            response = requests.request("POST", url, headers=headers, data = payload, files = files)

            print(response.text.encode('utf8'))
            data=response.text.encode('utf8')
            datadict=json.loads(data.decode('utf-8'))

            id=datadict['otp_id']
            status=datadict['status']
            print('id:',id)
            request.session['id'] = id
            return render(request,'otp.html')

        else:
            messages.error(request,'number not registerd')
            return render(request,'mobile.html')

    return render(request, 'mobile.html')

# {"otp_id":"6939d5de-8517-4788-b556-054404497e8d","status":"open","expiry":900}'          
    


def otp(request):
    if request.method == 'POST':
        otp=request.POST['otp']
       
        id=request.session['id']
        url = "https://d7networks.com/api/verifier/verify"

        payload = {'otp_id': id,
        'otp_code': otp}
        files = [

        ]
        headers = {
        'Authorization': 'Token 0d21f1e3cb977b24ebd925ec71d3fec0cb0a41f3'
        }

        response = requests.request("POST", url, headers=headers, data = payload, files = files)

        print(response.text.encode('utf8'))
        data=response.text.encode('utf8')
        datadict=json.loads(data.decode('utf-8'))
        status=datadict['status']
        
        if status=='success':
            username = request.session['username']   
            password =  request.session['password']
            dic=authenticate(username=username,password=password)
            auth.login(request,dic)
            return redirect(index)

        else:
            messages.error(request,'Incorrect OTP')
            return render(request,'otp.html')

    return render(request,'otp.html')



def index(request):
    if request.user.is_authenticated:
        user=request.user
        name=request.user.email
        customer,created = Customer.objects.get_or_create(user=user,name=name)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items= []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items'] 

    productitems = Product.objects.all()
    context = {'productitems' : productitems, 'cartItems':cartItems}
    return render(request, 'index.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items= []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items':items,'order':order, 'cartItems':cartItems}
    return render(request, 'checkout.html', context)



def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items= []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items':items,'order':order, 'cartItems':cartItems}
    return render(request, 'productcart.html', context)



def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print('User is not logged in..')
    return JsonResponse('Payment complete', safe=False)



def logout(request):
    auth.logout(request)
    return redirect(index)



def login(request):
    if request.user.is_authenticated:
        return redirect('index')

    elif request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect(index)
        else:
            messages.error(request, '😢 Wrong username/password!')
            return redirect('login')
    else:
        return render(request,'login.html')



def register(request):
    if request.user.is_authenticated:
        return redirect(index)

    elif request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        dicti = {"username":username,"email":email,"mobile":mobile}
        if password == confirmpassword:
            if User.objects.filter(email=email).exists():
                messages.error(request,'Email already taken')
                return render(request,'register.html',dicti)
            elif User.objects.filter(username=username).exists():
                messages.error(request,"username already taken") 
                return render(request,'register.html',dicti)
            else:
                user = User.objects.create_user(username=username, password=password, email=email, last_name=mobile, first_name=password)
                user.save();
                print("USER CREATED")
                return redirect(login)
        else:
            messages.error(request,'Password wrong')
            return render(request,'register.html',dicti)
    else:
        return render(request, 'register.html')


#admin 

def adminout(request):
    if request.session.has_key('password'):
        request.session.delete()
    else:
        pass
    return redirect(adminlogin)


#admin 

def adminlogin(request):
    if request.session.has_key('password'):
        password = request.session['password']
        return redirect('adminds')

    elif request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']

        if username == 'thanseef' and password == '1234':
            request.session['password'] = password
            return redirect('adminds')

        else:
            messages.error(request, '😢 Wrong username/password!')
            return redirect(adminlogin)
    else:
        return render(request,'adminlogin.html')

#admin 

def adminds(request):
    if request.session.has_key('password'):
        password = request.session['password']
        productitems = Product.objects.all()
        return render(request, 'admindashboard.html', {'productitems':productitems})
    else:
        return render(request,'adminlogin.html')

#admin 

def orders(request):
    if request.session.has_key('password'):
        password = request.session['password']
        productitems = Product.objects.all()
        return render(request,'order.html', {'productitems' : productitems})
    else:
        return render(request,'order.html')


#admin 

def adminpd(request):
    if request.session.has_key('password'):
        password = request.session['password']
        productitems = Product.objects.all()
        return render(request,'products.html', {'productitems' : productitems})
    else:
        return render(request,'products.html')



# def adminproduct(request):
#     if request.session.has_key('password'):
#         password = request.session['password']
#         productitems = Product.objects.all()
#         return render(request, 'adminproduct.html', {'productitems' : productitems})
#     else:
#         return render(request,'adminlogin.html')



def productview(request,id):
    prodview = Product.objects.get(id=id)
    return render(request, 'product.html',{'prodview' : prodview})


#admin 

def delete(request,id):
    product= Product.objects.get(id=id)
    product.delete()
    return redirect('adminpd')


#admin 

def addproduct(request):
    if request.method == "POST":
        name = request.POST['name']
        category = request.POST['category']
        product_quantity = request.POST['product_quantity']
        features = request.POST['features']
        oldprice = request.POST['oldprice']
        newprice = request.POST['newprice']
        image = request.POST['image']
        imagepr1 = request.POST['imagepr1']
        imagepr2 = request.POST['imagepr2']
        imagepr3 = request.POST['imagepr3']
        imagepr4 = request.POST['imagepr4']
        description = request.POST['description']
        prod = Product(description=description,imagepr4=imagepr4,imagepr3=imagepr3,imagepr2=imagepr2,imagepr1=imagepr1,image=image,name=name,product_quantity=product_quantity,category=category,features=features,oldprice=oldprice,newprice=newprice)
        prod.save();
        return redirect('adminpd')
    else:
        return render(request, 'productadd.html')


#admin 

def update(request,id):
    product=Product.objects.get(id=id)
    if request.method == 'POST':
        product.name=request.POST['name']
        product.category=request.POST['category']
        product.product_quantity=request.POST['product_quantity']
        product.features=request.POST['features']
        product.oldprice=request.POST['oldprice']
        product.newprice=request.POST['newprice']
        product.image=request.POST['image']
        product.imagepr1=request.POST['imagepr1']
        product.imagepr2=request.POST['imagepr2']
        product.imagepr3=request.POST['imagepr3']
        product.imagepr4=request.POST['imagepr4']
        product.description = request.POST['description']
        product.save()
        return redirect(adminpd)

    else:
        return render(request, 'updatepd.html', {'product':product})



# dicti = {"name":name,"category":category,"product_quantity":product_quantity,"attribute":attribute,"oldprice":oldprice,,"oldprice":oldprice}
        # if Product.objects.filter(name=name).exists():
        #     messages.error(request,'Product name exist')
        #     return render(request,'addproduct.html',dicti)


# @cache_control(no_cache=True, must_revalidate=True,no_store=True)
#  def adminhome(request):
#     if request.session.has_key('username'):
#         username = request.session['username']
#         return render(request, 'adminhome.html', {"username" : username})
#     else:
#         return render(request, 'adminlogin.html', {})


# def delete(request,id):
#     productitems = product.objects.get(id=id)
#     productitems.delete()
#     return redirect(adminproduct)


# def update(request,id):
#     productitems = product.objects.get(id=id)
#     if request.method=='POST':
#         first_name = request.POST['firstname']
#         last_name = request.POST['lastname']
#         email = request.POST['email']
#         user.first_name=first_name
#         user.last_name=last_name
#         user.email=email
#         user.save()
#         return redirect(adminlog)
#     else:
#         return render(request,'update.html',{'user':user})



# def adhome(request):
#     productitems = Product.objects.all()
#     return render(request, 'adhome.html', {'productitems' : productitems})


# request.session.flush()