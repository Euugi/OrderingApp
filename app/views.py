from django.http import HttpResponse
from django.contrib.auth import login
from django.shortcuts import render, HttpResponse, redirect, resolve_url
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages  # import messages
# dodać formularze od restuaracji
from .forms import DishForm, RestaurantForm, ReviewForm, SignUpForm, SignInForm
from .models import CustomUser, Dish, Message, Restaurant, Order, Supplier, Review
from django.views.generic import TemplateView


def index(request):
    return render(request, 'index.html')


@login_required
def dashboard(request):
    args = {}
    args['user_role'] = request.user.user_role
    args['user_name'] = request.user.first_name
    args['user_surname'] = request.user.last_name
    #args['user_role'] = request.user.user_role
    role = args['user_role']
    if role == 'restaurant':
        args['restaurants'] = Restaurant.objects.filter(owner=request.user.id)
        user_orders = []
        all_orders = Order.objects.all()
        for order in all_orders:
            for restaurant in args['restaurants']:
                if order.restaurant == restaurant:
                    user_orders.append(order)
        args['orders'] = user_orders
        return render(request, 'dashboard_restaurant.html', args)
    elif role == 'customer':
        args['orders'] = Order.objects.filter(ordered_user=request.user.id)
        return render(request, 'dashboard_customer.html', args)
    elif role == 'supplier':
        args['available_orders'] = Order.objects.filter(restaurant_acceptance='accepted', supplier_acceptance='awaiting')
        args['accepted_orders'] = Order.objects.filter(supplier=request.user.id)
        args['orders'] = Order.objects.filter(restaurant_acceptance='accepted')
        return render(request, 'dashboard_supplier.html', args)


def signUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            login(request, user)
            return HttpResponseRedirect(request.GET.get('next', 'http://127.0.0.1:8000/dashboard/'))
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def signIn(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(request.GET.get('next', 'http://127.0.0.1:8000/dashboard/'))
            else:
                return HttpResponseRedirect(request.GET.get('next', 'http://127.0.0.1:8000/login/error'))
    else:
        form = SignInForm()
    return render(request, 'login.html', {'form': form})


def loginError(request):
    return render(request, 'login_error.html')


@login_required
def logIn(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')


@login_required
def logOut(request):
    logout(request)
    return render(request, 'logout.html')


def signUpSuccess(request):
    return render(request, 'register_success.html')


def addRestaurant(request):
    if request.method == 'POST':
        form_restaurant = RestaurantForm(request.POST)
        if form_restaurant.is_valid():
            form_restaurant = form_restaurant.save(False)
            form_restaurant.owner = request.user
            form_restaurant.save()
            return HttpResponseRedirect(request.GET.get('next', 'http://127.0.0.1:8000/dashboard'))
            # return render(request, 'dashboard.html')
        else:
            return render(request, 'add_restaurant.html', {'form': form_restaurant})
    else:
        form_restaurant = RestaurantForm()
        return render(request, 'add_restaurant.html', {'form': form_restaurant})


def displayRestaurant(request, slug):
    args = {}
    args['restaurant'] = Restaurant.objects.get(slug=slug)
    args['dishes'] = Dish.objects.filter(restaurant_id=args['restaurant'].id)
    role = request.user.user_role
    if role == 'restaurant':
        return render(request, 'view_restaurant_owner.html', args)
    elif role == 'customer':
        return render(request, 'view_restaurant.html', args)

def addDish(request, slug):
    if request.method == 'POST':
        form_dish = DishForm(request.POST)
        if form_dish.is_valid():
            form_dish = form_dish.save(False)
            restaurant = Restaurant.objects.get(slug=slug)
            form_dish.restaurant_id = restaurant
            form_dish.save()
            return redirect('view_restaurant', slug)
            # return render(request, 'dashboard.html')
    else:
        form_dish = DishForm()
        return render(request, 'add_dish.html', {'form': form_dish})


def displayRestaurants(request):
    args = {}
    args['restaurants'] = Restaurant.objects.all()
    return render(request, 'display_restaurants.html', args)


def makeOrder(request, slug):
    if request.method == 'POST':
        order_items = {
        'items': []
        }
        #addr = request.POST.get('delivery_address')
        items = request.POST.getlist('items[]')
        for item in items:
            dish = Dish.objects.get(id__contains=int(item))
            item_data = {
                'id': dish.id,
                'name': dish.name,
                'price': dish.price,
            }
            order_items['items'].append(item_data)

        price = 0
        item_ids = []
        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])
        price = round(price, 2)
        order = Order.objects.create(price=price)
        order.items.add(*item_ids)
        order.ordered_user = request.user
        order.delivery_address = request.POST.get('delivery_address')
        order.restaurant_acceptance = 'awaiting'
        order.restaurant = Restaurant.objects.get(slug=slug)
        order.order_status = 'awaiting'
        # TYMCZASOWO
        order.save()
        args_order = {
            'items': order_items['items'],
            'price': price
        }
        #return HttpResponseRedirect(request.GET.get('next', 'http://127.0.0.1:8000/dashboard/order/'))
        return render(request, 'order_confirmation.html', args_order)
    else:
        args = {}
        args['restaurant'] = Restaurant.objects.get(slug=slug)
        args['dishes'] = Dish.objects.filter(restaurant_id=args['restaurant'])
        return render(request, 'view_restaurant.html', args)


def viewPlacedOrder(request, args):
    return render(request, 'order_confirmation.html', args)



def displayOrder(request, order_id):
    args = {}
    args['order'] = Order.objects.get(id=order_id)
    order = Order.objects.get(id=order_id)
    if order.review_id != None:
        args['is_reviewed'] = True
    args['messages'] = Message.objects.filter(room=order_id)
    role = request.user.user_role
    if order.review != None:
        args['is_reviewed'] = True
    if role == 'restaurant':
        supplier = order.supplier
        if supplier != None:
            args['supplier_name'] = supplier.username
        customer = CustomUser.objects.get(id=order.ordered_user_id)
        args['customer_name'] = customer.username
        if request.method == 'POST':
            confirmation = request.POST.get('confirmation')
            order.restaurant_acceptance = 'accepted'
            order.save()
            args['order'] = Order.objects.get(id=order_id)
            args['dishes'] = order.items.all()
            return render(request, 'order_details_restaurant.html', args)
        else:
            args['order'] = Order.objects.get(id=order_id)
            args['dishes'] = order.items.all()
            return render(request, 'order_details_restaurant.html', args)
    elif role == 'customer':
        supplier = order.supplier
        if supplier != None:
            args['supplier_name'] = supplier.username
        restaurant = Restaurant.objects.get(id=order.restaurant_id)
        if restaurant != None:
            restaurant_owner = restaurant.owner
        args['restaurant_owner_name'] = restaurant_owner.username
        if request.method == 'POST':
            confirmation = request.POST.get('confirmation')
            order.order_status = 'finished'
            order.save()
            args['dishes'] = order.items.all()
            args['order'] = Order.objects.get(id=order_id)
            return render(request, 'order_details_customer.html', args)
        else:
            args['dishes'] = order.items.all()
            return render(request, 'order_details_customer.html', args)
    elif role == 'supplier':
        customer = CustomUser.objects.get(id=order.ordered_user_id)
        args['customer_name'] = customer.username
        restaurant = Restaurant.objects.get(id=order.restaurant_id)
        restaurant_owner = restaurant.owner
        args['restaurant_owner_name'] = restaurant_owner.username
        if request.method == 'POST':
            confirmation = request.POST.get('confirmation')
            order.supplier_acceptance = 'accepted'
            order.order_status = 'in_progress'
            order.supplier = CustomUser.objects.get(id=request.user.id)
            order.save()
            args['order'] = Order.objects.get(id=order_id)
            return render(request, 'order_details_supplier.html', args)
        else:
            args['order'] = Order.objects.get(id=order_id)
            return render(request, 'order_details_supplier.html', args)


def displayReview(request, order_id):
    args = {}
    order = Order.objects.get(id=order_id)
    args['order'] = order
    if order.review_id != None:
        args['review'] = Review.objects.get(id=order.review_id)
        args['is_reviewed'] = True
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        review_form = review_form.save(False)
        review_form.save()
        order.review = review_form
        order.save()
        link = 'http://127.0.0.1:8000/dashboard/order/' + str(order_id)
        return HttpResponseRedirect(request.GET.get('next', link))
    else:
        args['form'] = ReviewForm()
        return render(request, 'order_review_customer.html', args)
