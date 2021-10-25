from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,Order,OrderItem
from django.contrib.auth.models import User
from django.views import View

# Create your views here.
def home(request):
    products = Product.objects.all()
    try:
        order = get_object_or_404(Order, user=request.user)
        items = OrderItem.objects.filter(order=order)
        items_list = [i.product.id for i in items]
    except:
        order={'get_item_total':0}
        items_list = []
    if request.user.is_authenticated:
        if request.method == 'POST':
            productId = request.POST.get("productId")
            user = request.user
            product = Product.objects.get(id=productId)
            order, created = Order.objects.get_or_create(user=user, complete=False)
            # items = OrderItem.objects.filter(order=order)
            # items_list = [str(i.product.id) for i in items]
            # if productId in items_list:
            #     orderitem = OrderItem.objects.get(order=order,product=product)
            # else:
            orderitem, created = OrderItem.objects.get_or_create(order=order,quantity=1, product=product)
            return redirect('cart:home')

    else:
        order = {'get_item_total':0}
    return render(request, "home.html",{'products':products,'order':order,'items_list':items_list})

def s_cart(request):
    try:
        order = get_object_or_404(Order, user=request.user)
        items = order.orderitem_set.all()
    except:
        order ={'get_item_total':0}
        items = []
    
    if request.method == 'POST':
        productId = request.POST.get("productId")
        operation = request.POST.get("operation")
        user = request.user
        product = Product.objects.get(id=productId)
        order = Order.objects.get(user=user, complete=False)
        orderitem = OrderItem.objects.get(order=order, product=product)
        if operation == 'add':
            orderitem.quantity = (orderitem.quantity +1)
        elif operation == 'sub':
            orderitem.quantity = (orderitem.quantity -1)
        orderitem.save()
        if orderitem.quantity <=0:
            orderitem.delete()
    return render(request, "cart.html",{'items':items,'order':order})