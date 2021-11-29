from django.contrib import messages
from django.contrib.auth import models #in thông báo 
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required #Kiểm tra login 
from django.contrib.auth.models import User #User của django 
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.forms import UserCreationForm #register
from django.db.models import Q # Search
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse #new
from django.core.paginator import EmptyPage, Paginator
import json #new
import datetime #new
from .models import *

# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')

    context={'page':page}
    return render(request, 'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #Chưa commit form mà giữ lại để chỉnh sữa data
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "Username Already Exits")

    context = {'form':form}
    return render(request, 'base/login_register.html', context)

def home(request):
    loop = range(5)
    books = Book.objects.all().order_by('-created')
    topbooks = Book.objects.all().order_by('-totalrating','-updated')[:4]
    try:
        book_fav = Book.objects.all().filter(favourites=request.user)
    except:
        book_fav = None
    category = Category.objects.all()
    reviews = Review.objects.all().order_by('-created')[:5]

    p = Paginator(books, 8)
    page_num = request.GET.get('page',1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    #new
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {'category':category, 'books':page, 'topbooks':topbooks,'book_fav': book_fav, 'reviews':reviews, 'p':range(p.num_pages+1), 'loop':loop, 'cartItems':cartItems}
    return render(request,'base/home.html', context)

def search(request):
    loop = range(5)
    reviews = Review.objects.all().order_by('-created')[:5]
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    books = Book.objects.filter(
        Q(category__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    category = Category.objects.all()
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {'category':category, 'books':books, 'reviews':reviews, 'loop':loop, 'cartItems':cartItems}
    return render(request,'base/search.html', context)

def getCategory(request, pk):
    category = Category.objects.all()
    book_category = Category.objects.get(id=pk)
    books = Book.objects.filter(category=book_category)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
    context = {'category':category, 'books':books, 'from':book_category, 'cartItems':cartItems}
    return render(request, 'base/category_component.html', context)

def getBook(request, pk):
    category = Category.objects.all()
    book = Book.objects.get(id=pk)
    book_review = book.review_set.all().order_by('-created')
    b_review = book.review_set.all().order_by('-created')
    reviews = book_review.order_by('-created')[:5]
    fav = bool
    
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
        
    if book.favourites.filter(id=request.user.id).exists():
        fav = True
    else:
        fav= False
    if request.method == 'POST' and request.POST.get('review')!='':
        for item in book_review:
                if item.customer == request.user and item.review_star !=0 :
                    book.totalrating -= int(item.review_star)
                    book.review_count -= 1
                    break
        book.totalrating = book.totalrating + int(request.POST.get('rate'))
        book.review_count += 1
        book.save()
        review = Review.objects.create(
            customer = request.user,
            review_text = request.POST.get('review'),
            book = book,
            review_star = request.POST.get('rate')
        )
    try:
        book.star = book.totalrating / book.review_count
        book.save()
    except:
        book.star = book.totalrating 
        book.save()

    book.star = round(book.star, 0)
    redirect('getbook',pk=book.id) 

    context = {'category':category, 'book':book, 'review':b_review, 'reviews':reviews, 'star': range(int(book.star)), 'fav':fav, 'cartItems':cartItems}
    return render(request,'base/book.html', context)

def getWriter(request, pk):
    category = Category.objects.all()
    writer = Writer.objects.get(id=pk)
    books = Book.objects.filter(writer=writer).order_by('-created') 
    topbooks = books.order_by('-totalrating')[:5]
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {'writer':writer, 'category':category, 'books':books, 'topbooks':topbooks, 'cartItems':cartItems}
    return render(request, 'base/writer.html', context)

@login_required(login_url='login')
def fav_add(request, pk):
    book = Book.objects.get(id=pk)
    if book.favourites.filter(id=request.user.id).exists():
        book.favourites.remove(request.user)
    else:
        book.favourites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def deleteReview(request, pk):
    try:
        review = Review.objects.get(id=pk)
    except:
        return redirect('home')
    book = review.book
    b_review = book.review_set.all().order_by('-created')
    i = 0
    for item in b_review:
        if review.customer == item.customer:
            i+=1
    if i == 1:
        book.totalrating -= int(review.review_star)
        book.review_count -= 1
        book.save()     
    if i > 1:
        for item in b_review:
            if review.customer == item.customer:
               if review == item:
                   book.totalrating -= int(review.review_star)
                   book.save()
                   j=0
                   for item2 in b_review:
                       if review.customer == item2.customer:
                           j+=1
                           if j ==2:
                               book.totalrating += int(item2.review_star)
                               book.save()
               else:
                   break
                    
    review.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
def fav_book(request):
    loop = range(5)
    reviews = Review.objects.all().filter(customer=request.user).order_by('-created')
    category = Category.objects.all()
    book_fav = Book.objects.all().filter(favourites=request.user)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
    context = {'category':category, 'books':book_fav, 'book_fav': book_fav, 'reviews':reviews, 'loop':loop, 'cartItems':cartItems}
    return render(request, 'base/fav_book.html', context)  


#new
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'base/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'base/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    bookId = data['bookId']
    action = data['action']
    print('Action:', action)
    print('Book:', bookId)
    customer = request.user
    book = Book.objects.get(id=bookId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, book=book)

    if action == 'add':
        if orderItem.quantity < book.stock:
            orderItem.quantity = (orderItem.quantity + 1)
    elif action =='remove':
        orderItem.quantity = (orderItem.quantity - 1)
    if action == "delete":
        orderItem.quantity = 0
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
        
    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        items = order.orderitem_set.all()

        if total == float(order.get_cart_total):
            order.complete = True
        order.save()
        
        for item in items:
            item.book.stock -= item.quantity
            item.book.save()

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
    return JsonResponse('Payment Complete!', safe=False)