from rest_framework import routers, serializers, viewsets
from . serializers import UserSerializer
from django.shortcuts import render, HttpResponse, redirect
from . models import *
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.


def index(request):
    if request.method == 'POST':
        product_id = request.POST.get('cartid')
        remove = request.POST.get('minus')
        cart_id = request.session.get('cart')
        if cart_id:
            quantity = cart_id.get(product_id)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart_id.pop(product_id)
                    else:
                        cart_id[product_id] = quantity - 1
                else:
                    cart_id[product_id] = quantity + 1
            else:
                cart_id[product_id] = 1
        else:
            cart_id = {}
            cart_id[product_id] = 1
        request.session['cart'] = cart_id
        # print("---------------", request.session['cart'])

    cat_id = request.GET.get('cat_id')
    cate = catagory.objects.all()
    if cat_id:
        pro = product.objects.filter(catagory=cat_id)
    else:
        pro = product.objects.all()
    context = {

        'catagory': cate,
        'product': pro
    }
    return render(request, 'home.html', context=context)


def contact(request):
    return render(request, 'contact.html')


def signup(request):
    if request.method == "POST":
        f_name = request.POST.get('fname')
        l_name = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        mobile = request.POST.get('ph')
        gender = request.POST.get('gender')

        S = Registration(
            first_name=f_name,
            last_name=l_name,
            email=email,
            password=make_password(password),
            mobile=mobile,
            gender=gender,
        )
        S.save()
        return redirect("home")
        # return HttpResponse("data save successfully")


def login(request):
    if request.method == "POST":
        email = request.POST.get('logeid')
        password = request.POST.get('password')
        try:
            fetch_obj = Registration.objects.get(email=email)
            if check_password(password, fetch_obj.password):
                # return HttpResponse("log in successfully")
                request.session['name'] = fetch_obj.first_name
                request.session['customer_id'] = fetch_obj.id
                return redirect('home')
            else:
                return HttpResponse("please insert a valid password")
        except:
            return HttpResponse("please insert correct email")


def logout(request):
    request.session.clear()
    return redirect('home')


def Cart_info(request):
    keys = list(request.session['cart'].keys())
    # print(keys)
    c = product.objects.filter(id__in=keys)
    return render(request, 'cart.html', {'cartdtls': c})


def checkout(request):
    if request.method == 'POST':
        address = request.POST.get('addr')
        mobile = request.POST.get('mbl')
        customer_id = request.session.get('customer_id')
        if not customer_id:
            return HttpResponse('plese Login')
        cart = request.session.get('cart')
        products = product.objects.filter(id__in=list(cart.keys()))
        for i in products:
            obj = Order_dtls(
                address=address,
                mobile=mobile,
                customer=Registration(id=customer_id),
                product=product(id=i.id),
                price=i.price,
                quantity=cart.get(str(i.id))

            )
            obj.save()
        request.session['cart'] = {}
        return redirect('order')


def order(request):
    id = request.session.get('customer_id')

    fetch_pro = Order_dtls.objects.filter(customer=id)
    tp = 0
    for i in fetch_pro:
        tp = tp+(i.price*i.quantity)
    return render(request, 'order.html', {'fetch_product': fetch_pro, 'tp': tp})


class UserViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = UserSerializer
