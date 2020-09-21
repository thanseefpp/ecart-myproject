from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('register',views.register,name='register'),
    path('admin/',views.adminlogin,name='adminlogin'),
    path('adminout',views.adminout,name = 'adminout'),
    path('logout',views.logout),
    path('addproduct',views.addproduct, name = 'addproduct'),
    path('adminproduct',views.adminproduct,name = 'adminproduct'),
    path("delete/<int:id>/",views.delete,name="delete" ),
    path("update/<int:id>/",views.update,name='update'),
    path("productview/<int:id>/",views.productview,name='productview'),

    
]
# path('adhome',views.adhome,name = 'adhome'),
# path('adminproduct',views.adminproduct,name='adminproduct'),
# 
# 
# path('adminhome',views.adminhome,name='adminhome'),
