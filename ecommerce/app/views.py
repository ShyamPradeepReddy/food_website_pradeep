from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.http import HttpResponse,JsonResponse
from django.core.files.storage import default_storage
from .models import Product,Cart
from django.views import View
from django.db.models import Count,Q
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from .models import Customer
# Create your views here.
# def home(request):
#     return HttpResponse("<h1>Hello World</h1>")
def home(request):
    return render(request,'app/home.html')
def about(request):
    return render(request,'app/about.html')
def contact(request):
    return render(request,'app/contact.html')
class CategoryView(View):
    def get(self,request,val):
        product=Product.objects.filter(category=val)
        # product1=Product.objects.get(category=val) not used due to multiple objects problem during retreival
        # t1=product1.title not used due to multiple objects problem during retreival
        title=Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())
class ProductDetails(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        return render(request,"app/productdetail.html",locals())
class CategoryTitle(View):
    def get(self,request,val):
        product=Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())
class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,"app/customerregistration.html",locals())
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulation user registration succesful")
            return redirect('login')
        else:
            messages.warning(request,"Invalid data")
        return render(request,"app/customerregistration.html",locals())
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,'app/profile.html',locals())
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulation sprofile saved succesfully")
            return redirect('/')
        else:
            messages.warning(request,"Invalid data")
        return render(request,'app/profile.html',locals())
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',locals())
class UpdateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)# to add data into the fields to update
        return render(request,'app/updateAddress.html',locals())
    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulation sprofile saved succesfully")
        else:
            messages.warning(request,"Invalid data")
        return redirect('address')
class MyLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
def add_to_cart(request):
    user=request.user
    product_id=request.POST.get('prod_id')
    # print(product_id,type(product_id))
    # product_id=int(product_id)
    if Cart.objects.filter(user=user,product=product_id).exists():
        c=Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        return redirect('/cart')
    else:
        product=Product.objects.get(id=product_id)
        Cart(user=user,product=product).save()
        return redirect("/cart")
def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.quantity*p.product.sellong_price
        amount=amount+value
    totalamount=amount+40
    return render(request,"app/addtocart.html",locals())
def plus_cart(request):
    if request.method=='GET':
        print("It is of plus")
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.sellong_price
            amount=amount+value
        totalamount=amount+40
        print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
def minus_cart(request):
    if request.method=='GET':
        print("It is of minus")
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.sellong_price
            amount=amount+value
        if c.quantity>=1:
            totalamount=amount+40
        else:
            totalamount=0
        print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.delete()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.sellong_price
            amount=amount+value
        totalamount=amount+40
        print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
class Checkout(View):
    def get(self,request):
        return render(request,'app/checkout.html',locals())
@csrf_exempt
def search_products(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(title__icontains=query)[:10]
        results = [{
            'id': p.id,
            'title': p.title,
            'selling_price': p.sellong_price,
            'discounted_price': p.discounted_price
        } for p in products]
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})
