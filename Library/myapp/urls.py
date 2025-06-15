from django.urls import path
from myapp import views

urlpatterns=[
    path('',views.index,name='index'),
    path('signin/',views.signin,name='signin'),
    path('login/',views.log_in,name='login'),
    path('home/',views.home,name='home'),
    path('desc/<int:id>',views.desc,name='desc'),
    path('borrow/<int:id>',views.borrow,name='borrow'),
    path('profile/',views.profile,name='profile'),
    path('books/',views.books,name='books'),
    path('delrec/<int:id>',views.delrec,name='delrec'),
    path('logout/',views.log_out,name='logout'),
]