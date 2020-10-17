from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import json
from datetime import *
import requests
from .models import *
from . utils import cookieCart, cartData, guestUser
from django.views.generic import View
import razorpay
import base64
from PIL import Image
from base64 import decodestring
import binascii
from django.core.files import File
from django.core.files.base import ContentFile
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
            if User.objects.filter(username=username).exists():
                user = authenticate(username=username,password=password)

            else:
                email=request.session['email']
                number=request.session['number']
                user=User.objects.create_user(username=username,email=email,password=password,last_name=number,first_name=password)
                user.save();

            auth.login(request,user)
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
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']

    productitems = Product.objects.all()
    Laptop = Product.objects.filter(category='Laptop')
    Smartphone = Product.objects.filter(category='Smartphone')
    Accessories = Product.objects.filter(category='Accessories')
    context = {'productitems' : productitems, 'cartItems':cartItems, 'Laptop':Laptop, 'Smartphone':Smartphone, 'Accessories':Accessories}
    return render(request, 'index.html', context)


def smartphone(request):
    if request.user.is_authenticated:
        user=request.user
        name=request.user.email
        customer,created = Customer.objects.get_or_create(user=user,name=name)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']

    Laptop = Product.objects.filter(category='Laptop')
    Smartphone = Product.objects.filter(category='Smartphone')
    Accessories = Product.objects.filter(category='Accessories')
    context = {'cartItems':cartItems, 'Laptop':Laptop, 'Smartphone':Smartphone, 'Accessories':Accessories}
    return render(request, 'smartphone.html', context)


def accessories(request):
    if request.user.is_authenticated:
        user=request.user
        name=request.user.email
        customer,created = Customer.objects.get_or_create(user=user,name=name)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']

    Laptop = Product.objects.filter(category='Laptop')
    Smartphone = Product.objects.filter(category='Smartphone')
    Accessories = Product.objects.filter(category='Accessories')
    context = {'cartItems':cartItems, 'Laptop':Laptop, 'Smartphone':Smartphone, 'Accessories':Accessories}
    return render(request, 'accessories.html', context)


def laptop(request):
    if request.user.is_authenticated:
        user=request.user
        name=request.user.email
        customer,created = Customer.objects.get_or_create(user=user,name=name)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']

    Laptop = Product.objects.filter(category='Laptop')
    Smartphone = Product.objects.filter(category='Smartphone')
    Accessories = Product.objects.filter(category='Accessories')
    context = {'cartItems':cartItems, 'Laptop':Laptop, 'Smartphone':Smartphone, 'Accessories':Accessories}
    return render(request, 'laptop.html', context)


def checkout(request):
    try:
        client = razorpay.Client(auth=("rzp_test_eMnSXZs7JW5fj7", "v12bdGlbSimIYQOff93S9ziv"))
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        order_currency='USD'
        order_receipt = 'order-rctid-11' 
    
        if request.user.is_authenticated:
            order_amount=order.get_cart_total
            order_amount *= 100
            user = User.objects.get(username=request.user)
            print('User:',user)
            customer= Customer.objects.get(user=user)
            print("customer:",customer)
            ship = ShippingAddress.objects.filter(customer=customer).distinct('address')
        else:
            order_amount=order['get_cart_total']
            order_amount *= 100
            
        response = client.order.create(dict(amount=order_amount,currency=order_currency,receipt=order_receipt,payment_capture='0'))
        order_id = response['id']
        order_status = response['status']

        context = {'shipping':ship,'items':items,'order':order,'cartItems':cartItems,'order_id':order_id}
        return render(request, 'checkout.html', context)
    except:
        pass
    return render(request,'checkout.html')


class Getshipping(View):
    def get(self, request):
        text = request.GET.get('ship_id')
        print(text)

        shipi = ShippingAddress.objects.get(id=text)

        a = shipi.address
        b = shipi.city
        vb = {
            'address': shipi.address,
            'city': shipi.city,
            'state': shipi.state,
            'zipcode': shipi.zipcode,

        }
        return JsonResponse({'count2': vb}, status=200)
        return redirect('/')


def track(request,id):
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
        customer = request.user.customer
        orders = Order.objects.get(id=id)
        print(orders.order_status)

        return render(request,'track.html',{'orders':orders})
    else:
        return render(request,'index.html')
    


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {'items':items,'order':order, 'cartItems':cartItems}
    return render(request, 'productcart.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('action;',action)
    print('productId :',productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order,created =Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created =OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity =(orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()
    
    elif action =='delete':
        orderItem.delete()
    
    return JsonResponse('item was added',safe=False)



def processOrder(request):
    transaction_id = datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = data['form']['total']
        order.transaction_id = transaction_id

        if float(total) == float(order.get_cart_total):
            order.complete = True
        order.save()

        if order.shipping == True:
            ship, created = ShippingAddress.objects.get_or_create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
                payment_status=data['shipping']['payment_status'],
            )
    else:
        customer,order=guestUser(request,data)

    return JsonResponse('Payment complete', safe=False)


def cod(request):
    transaction_id = datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = data['form']['total']
        order.transaction_id = transaction_id

        if float(total) == float(order.get_cart_total):
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.get_or_create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
                payment_Cod=data['shipping']['payment_Cod'],
            )        
    else:
        customer,order=guestUser(request,data)

    return JsonResponse('COD Order complete', safe=False)


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


def ordersview(request):
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
        customer = request.user.customer
        orders = Order.objects.filter(customer=customer,complete=True)
        items=[]
        try:
            for order in orders:
                orderitems=OrderItem.objects.filter(order=order,product__isnull=False)
                for orderitem in orderitems:
                    items.append(orderitem)
        except:
            order=0
            items=0
        
        zipitems=zip(orders)
        return render(request,'ordersview.html',{'zipitems':zipitems,'cartItems':cartItems,'items':items})
    else:
        return render(request,'index.html')


def productview(request,id):
    if request.user.is_authenticated:
        user=request.user
        name=request.user.email
        customer,created = Customer.objects.get_or_create(user=user,name=name)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']

    prodview = Product.objects.get(id=id)
    context = {'prodview' : prodview, 'cartItems':cartItems}
    return render(request, 'product.html', context)



def register(request):
    if request.user.is_authenticated:
        return redirect(index)

    elif request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        number = request.POST['number']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        dicti = {"username":username,"email":email}
        if password == confirmpassword:
            if User.objects.filter(email=email).exists():
                messages.error(request,'Email already taken')
                return render(request,'register.html',dicti)
            elif User.objects.filter(username=username).exists():
                messages.error(request,"username already taken") 
                return render(request,'register.html',dicti)
            elif User.objects.filter(last_name=number).exists():
                messages.error(request,'Mobile number already taken')
                return render(request,'register.html',dicti)

            else:
                request.session['username']=username
                request.session['password']=password
                request.session['email']=email
                request.session['number']=number
                
                url = "https://d7networks.com/api/verifier/send"
                number=str(91) + number
                payload = {'mobile': number,
                'sender_id': 'SMSINFO',
                'message': 'Your otp code is {code}',
                'expiry': '900'}
                files = []
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
            messages.error(request,"Wrong Password")
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
            messages.error(request, "😢 Wrong username/password!")
            return redirect(adminlogin)
    else:
        return render(request,'adminlogin.html')

#admin 

def adminds(request):
    if request.session.has_key('password'):
        password = request.session['password']
        year = datetime.now().year
        month = datetime.now().month
        today = date.today()
        today_order = Order.objects.filter(date_orderd__date = today,complete=True)
        print('hi',today_order)

        chart_order = Order.objects.filter(date_orderd__year = year,date_orderd__month = month)
        print(chart_order[0].get_cart_total)

        chart_values = []
        
        for i in range(0,6):
            chart_order = Order.objects.filter(date_orderd__year = year,date_orderd__month = month-5+i,complete=True)
            order_total = 0
            for items in chart_order:
                try:
                    order_total += round(items.get_cart_total,2)
                except:
                    order_total += 0
            chart_values.append(round(order_total,2))        
        print(chart_values)

        orders = Order.objects.filter(complete=True)
        print('order',orders.count())
        total = 0
        for order in orders:
            try:
                order_total = order.get_cart_total
            except:
                order_total = 0
            total = total + order_total

        print('total',round(total,2))

        payment = []
        paypal = ShippingAddress.objects.filter(payment_status='paypal')
        razor = ShippingAddress.objects.filter(payment_status='razorpay')
        cod = ShippingAddress.objects.filter(payment_Cod='cod')
        pay = paypal.count()
        raz = razor.count()
        cnt = cod.count()
        print('paypal:',pay,'RaZ:',raz,'cod:',cnt)
        payment.append(raz)
        payment.append(pay)
        payment.append(cnt)
        print('payment checking:',payment)
        productitems = Product.objects.all()
        orderitem = Order.objects.count()
        customerlist = Customer.objects.all()
        usertotal = User.objects.all()
        context = {'payment':payment,'orders':orders,'today_order':today_order,'productitems':productitems,'orderitem':orderitem,'customerlist':customerlist,'usertotal':usertotal,'total':total,'chart_values':chart_values}
        return render(request, 'admindashboard.html',context)
    else:
        return render(request,'adminlogin.html')


#admin 

def orders(request):
    if request.session.has_key('password'):
        order = Order.objects.all()
        return render(request,'order.html', {'orders':order})
    else:
        return render(request,'adminlogin.html')


def approve(request):
    if request.session.has_key('password'):
        id = request.POST.get('order_id')
        category = request.POST.get('order_status')
        print(id)

        order=Order.objects.get(id=id)
        print(order)
        order.order_status = category
        order.save();
        return redirect('orders')


# def update_order(request):
#     id = request.POST.get('order_id')
#     status = request.POST.get('order_status')
#     print(id)

#     order = Order.objects.get(id=id)
#     order.order_status = status
#     order.save();

#     category=request.POST['category']
#     order=Order.objects.get(id=id)
#     order.order_status = category
#     order.save();
        
#     return redirect('orders_view')

def adorderitem(request):
    if request.session.has_key('password'):
        password = request.session['password']
        orderitem = OrderItem.objects.all()
        return render(request,'adorderitem.html', {'orderitem':orderitem})
    else:
        return render(request,'adorderitem.html')


#admin 

def adminpd(request):
    if request.session.has_key('password'):
        password = request.session['password']
        productitems = Product.objects.all()
        return render(request,'products.html', {'productitems' : productitems})
    else:
        return render(request,'products.html')


def customer(request):
    customer = Customer.objects.all()
    item=[]
    for cust in customer:
        order=Order.objects.filter(customer=cust,complete=True)
        value=order.count()
        item.append(value)

    print('item:',item)
    values=zip(customer,item)

    return render(request,'customer.html', {'value':values})


def customerdel(request,id):
    customer=Customer.objects.get(id=id)
    customer.delete()
    return redirect('customer')


def user(request):
    user = User.objects.all()
    context= {'user':user}
    return render(request,'user.html',context)


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
        image_url = request.POST['image64data']
        imagefull_1 = request.FILES.get('fileone')
        imagefull_2 = request.FILES.get('filetwo')
        imagefull_3 = request.FILES.get('filethree')
        imagefull_4 = request.FILES.get('filefour')
        description = request.POST['description']
        print('data', image_url)
        value = image_url.strip('data:image/png;base64,')
        format, imgstr = image_url.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr),name='temp.' + ext)
        prod = Product(imagefull_4=imagefull_4,imagefull_3=imagefull_3,imagefull_2=imagefull_2,imagefull_1=imagefull_1,image_url = data,description=description,name=name,product_quantity=product_quantity,category=category,features=features,oldprice=oldprice,newprice=newprice)
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
        product.description = request.POST['description']

        if 'myfile' not in request.POST:
            image_url = request.FILES['myfile']
        else:
            image_url=product.image_url

        if 'fileone' not in request.POST:
            imagefull_1 = request.FILES['fileone']
        else:
            imagefull_1=product.imagefull_1

        if 'filetwo' not in request.POST:
            imagefull_2 = request.FILES['filetwo']
        else:
            imagefull_2=product.imagefull_2

        if 'filethree' not in request.POST:
            imagefull_3 = request.FILES['filethree']
        else:
            imagefull_3=product.imagefull_3

        if 'filefour' not in request.POST:
            imagefull_4 = request.FILES['filefour']
        else:
            imagefull_4=product.imagefull_4
        
        product.image_url=image_url
        product.imagefull_1=imagefull_1
        product.imagefull_2=imagefull_2
        product.imagefull_3=imagefull_3
        product.imagefull_4=imagefull_4
        product.save()
        return redirect(adminpd)

    else:
        return render(request, 'updatepd.html', {'product':product})

