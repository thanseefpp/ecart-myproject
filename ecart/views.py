from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control
from .models import Product
# Create your views here.


def index(request):
    productitems = Product.objects.all()
    return render(request, 'index.html', {'productitems' : productitems})


def logout(request):
    response =redirect(index)
    response.delete_cookie('user')
    return response



def login(request):
    if request.COOKIES.get('user'):
        return render(request,'index.html')

    elif request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            response = redirect(index)
            response.set_cookie('user','user')
            return response
        else:
            messages.error(request, '😢 Wrong username/password!')
            return redirect('login')
    else:
        return render(request,'login.html')



def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
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
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save();
                print("USER CREATED")
                return redirect(login)
        else:
            messages.error(request,'Password wrong')
            return render(request,'register.html',dicti)
    else:
        return render(request, 'register.html')




def adminout(request):
    if request.session.has_key('password'):
        request.session.delete()
    else:
        pass
    return redirect(adminlogin)




def adminlogin(request):
    if request.session.has_key('password'):
        password = request.session['password']
        return redirect('adminproduct')

    elif request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']

        if username == 'thanseef' and password == '1234':
            request.session['password'] = password
            return redirect('adminproduct')

        else:
            messages.error(request, '😢 Wrong username/password!')
            return redirect(adminlogin)
    else:
        return render(request,'adminlogin.html')



def adminproduct(request):
    if request.session.has_key('password'):
        password = request.session['password']
        productitems = Product.objects.all()
        return render(request, 'adminproduct.html', {'productitems' : productitems})
    else:
        return render(request,'adminlogin.html')



def productview(request,id):
    prodview = Product.objects.get(id=id)
    return render(request, 'product.html',{'prodview' : prodview})



def delete(request,id):
    product= Product.objects.get(id=id)
    product.delete()
    return redirect('adminproduct')



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
        return redirect('adminproduct')
    else:
        return render(request, 'addproduct.html')



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
        return redirect(adminproduct)

    else:
        return render(request, 'updateproduct.html', {'product':product})



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