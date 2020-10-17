from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('smartphone/',views.smartphone,name='smartphone'),
    path('accessories/',views.accessories,name='accessories'),
    path('laptop/',views.laptop,name='laptop'),
    path('login/',views.login,name='login'),
    path('register',views.register,name='register'),
    path('admin/',views.adminlogin,name='adminlogin'),
    path('adminout',views.adminout,name = 'adminout'),
    path('logout/',views.logout,name='logout'),
    path('addproduct',views.addproduct, name = 'addproduct'),
    path("delete/<int:id>/",views.delete,name="delete" ),
    path("update/<int:id>/",views.update,name='update'),
    path("productview/<int:id>/",views.productview,name='productview'),
    path('adminpd',views.adminpd,name='adminpd'),
    path('adminds',views.adminds,name='adminds'),
    path('orders',views.orders,name='orders'),
    path('checkout/',views.checkout,name='checkout'),
    path('cart/',views.cart,name='cart'),
    path('update_item/',views.updateItem,name='update_item'),
    path('process_order/',views.processOrder,name='process_order'),
    path('mobile/',views.mobile,name='mobile'),
    path('otp/',views.otp,name='otp'),
    path('customer/',views.customer,name='customer'),
    path('user/',views.user,name='user'),
    path('ordersview/',views.ordersview,name='ordersview'),
    path('adorderitem/',views.adorderitem,name='adorderitem'),
    path('approve/<int:id>/',views.approve,name='approve'),
    path('customerdel/<int:id>/',views.customerdel,name='customerdel'),
    path('cod/',views.cod,name='cod'),
    path('getshipping/',views.Getshipping.as_view()),
    path('track/<int:id>/',views.track,name='track'),

]



# path('adhome',views.adhome,name = 'adhome'),
# path('adminproduct',views.adminproduct,name='adminproduct'),
# path('adminproduct',views.adminproduct,name = 'adminproduct'),
# 
# path('adminhome',views.adminhome,name='adminhome'),
