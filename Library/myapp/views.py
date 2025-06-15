from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User
from .models import Book,Borrowed
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request,'index.html')

def signin(request,method=['POST','GET']):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
        user.set_password(password)
        user.save()
        return redirect('/login/')
    
    return render(request,'signin.html')

def log_in(request,method=['POST','GET']):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(email=email):
            messages.info(request,'Invalid email')
        else:
            user = authenticate(username=username,password=password)
            if user is None:
                messages.info(request,'Wrong Password...')
            else:
                login(request,user)
                request.session['email']=email
                request.session['username']=username
                return redirect('/home/')
    return render(request,'login.html')

def home(request):
    books = Book.objects.all()
    return render(request,'home.html',{'books':books})

def profile(request):
    email = request.session['email']
    username = request.session['username']
    detail = User.objects.get(email=email)
    detail1 = Borrowed.objects.filter(username=username).count()
    return render(request,'profile.html',{'detail':detail,'detail1':detail1})

def desc(request,id):
    books = Book.objects.get(id=id)
    return render(request,'desc.html',{'books':books,'id':id})

def borrow(request,id):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        firstdate = request.POST.get('firstdate')
        lastdate = request.POST.get('lastdate')
        bookname = Book.objects.get(id=id)
        counts = Borrowed.objects.filter(username=username).count()

        if username is None:
            messages.info(request,'Fill the form completely...')
        elif email is None:
            messages.info(request,'Fill the form completely...')
        elif firstdate and lastdate is None:
            messages.info(request,'Fill the form completely...')
        elif counts < 2:
            fdate = Borrowed.objects.filter(firstdate=firstdate)
            bkid = Borrowed.objects.filter(bookname=bookname)
            bkdate = Borrowed.objects.filter(bookname=bookname).values('firstdate')

            if bkid.exists():
                if bkdate.exists():
                    messages.info(request,'Someone Already Borrowed in this Date...')
                else:
                    messages.info(request,'Book Already Borrowed...')
            else:
                Borrowed.objects.create(email=email,username=username,firstdate=firstdate,lastdate=lastdate,bookname=bookname)
                return redirect('/home/')
        else:
            messages.info(request,'Borrowed Limit reached...')
    context={
        'id':id
    }
    return render(request,'borrow.html',context)

def books(request):
    username = request.session['username']
    books = Borrowed.objects.filter(username=username)

    bkdetail =[]

    for b in books:
        info = Book.objects.filter(bookname = b.bookname).first()

        if info :
            bkdetail.append({
                "id" : b.id,
                "bookname" : info.bookname,
                "author" : info.author,
                "bookimg" : info.bookimg.url,
                "booklink" : info.book.url,
            })        

    return render(request,'books.html',{'bkdetail':bkdetail})

def delrec(request,id):
    record = get_object_or_404(Borrowed,id=id)
    record.delete()
    return redirect('/books/')  
   
def log_out(request):
    logout(request)
    return redirect('/')