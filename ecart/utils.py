import json
from . models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart:',cart)
    items= []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = (product.newprice * cart[i]["quantity"])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]
            
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'newprice':product.newprice,
                    'image':product.image,
                },
                'quantity':cart[i]["quantity"],
                'get_total':total
                }
            items.append(item)
        except:
            pass
    return{'items':items,'order':order, 'cartItems':cartItems}