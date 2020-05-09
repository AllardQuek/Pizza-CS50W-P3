import os
import stripe

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Pizza, Sub, Pasta, Salad, DinnerPlatter, CartItem, Topping, Addition

# Create your views here.
def index(request):
    # If logged in show login/register page
    if not request.user.is_authenticated:
        return render(request, "users/login.html")

    # Else show homepage
    return render(request, "users/user.html", {
        "user": request.user,
        "pizzas": Pizza.objects.all(),
        "toppings": Topping.objects.all(),
        "subs": Sub.objects.all(),
        "additions": Addition.objects.all(), 
        "pastas": Pasta.objects.all(),
        "salads": Salad.objects.all(),
        "dinnerplatters": DinnerPlatter.objects.all()
    })


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "users/login.html", {"message": "Invalid credentials"})


def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {"message": "Logged out successfully!"})


def register_view(request):
    username = request.POST['username']
    password = request.POST['password']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    email = request.POST['email']
    user = User.objects.create_user(username, email, password)
    user.first_name = firstname
    user.last_name = lastname
    user.save()

    # Go ahead and log user in and display the menu
    login(request, user)
    return HttpResponseRedirect(reverse("index"))


def cart(request):
    # This is a sample test API key. Sign in to see examples pre-filled with your key.
    if not os.getenv("SECRET_STRIPE_KEY"):
        raise RuntimeError("SECRET_STRIPE_KEY is not set")

    stripe.api_key = os.getenv("SECRET_STRIPE_KEY")

    # Query for a list of all the user's cart items
    all_items = CartItem.objects.filter(user=request.user).exclude(item_type__in=["Addition", "Topping"])
    
    # Calculate total cost of cart items
    if all_items:
        total_cost = 0
        for i in all_items:
            total_cost += i.price
        cost_string = str(total_cost)

        intent = stripe.PaymentIntent.create(
            amount=int(cost_string.replace('.', '')),
            currency='sgd'
        )

        return render(request, "orders/cart.html", {
            "user": request.user,
            "items": all_items,
            "total_cost": total_cost,
            "client_secret": intent.client_secret,
            "data_user": request.user
        })
    else:
        return render(request, "orders/cart.html", {
        "user": request.user,
        })

def add_to_cart(request):
    # Add new cart item
    if request.method == "POST":
        print(request.POST)
        p_id = request.POST["pizza"] 
        p = Pizza.objects.get(pk=p_id)

        # Evaluate user's complete item including any toppings
        # https://stackoverflow.com/questions/1630320/what-is-the-pythonic-way-to-detect-the-last-element-in-a-for-loop
        # print(str(p.p_type), type(p.p_type))
        if "Topping" in str(p.p_type):
            # https://stackoverflow.com/questions/36282016/cant-extract-list-from-querydict-in-django
            topping_list = request.POST.getlist('topping')
            print(topping_list)
            toppings = ''
            first = True

            for i in topping_list:
                top = Topping.objects.get(pk=i)
                top_cartitem = CartItem(item=top, user=request.user, item_type="Topping", item_id=top.id, price=0)
                top_cartitem.save()

                if first:
                    toppings += top.topping
                    first = False
                else:
                    toppings += ', ' + top.topping
            full_item = f"{p} with toppings {toppings}"
        elif p.p_type == "Special":
            full_item = f"{p} with Black Olives, Fresh Garlic, Zucchini"
        else:
            full_item = f"{p}"
        
        cartitem = CartItem(item=full_item, user=request.user, item_type="Pizza", item_id=p.id, price=p.price)
        cartitem.save()

    return HttpResponseRedirect(reverse("cart"))

def add_sub(request):
    if request.method == "POST":
        print(request.POST)
        sub_id = request.POST["sub"] 
        sub = Sub.objects.get(pk=sub_id)
        total_price = sub.price
        # If user selected any additions, length of QueryDict will be > 2 
        if len(request.POST) > 2:
            add_list = request.POST.getlist('addition')
            print(add_list)
            additions = ''
            first = True

            for i in add_list:
                addn = Addition.objects.get(pk=i)
                total_price += addn.price
                addn_cartitem = CartItem(item=addn, user=request.user, item_type="Addition", item_id=addn.id, price=addn.price)
                addn_cartitem.save()

                if first:
                    additions += addn.addition
                    first = False
                else:
                    additions += ', ' + addn.addition
            full_item = f"{additions} on {sub.size} {sub.sub_type} sub: {total_price}"
        else:
            full_item = f"{sub}"

        # Save the sub as a CartItem
        cartitem = CartItem(item=full_item, user=request.user, item_type="Sub", item_id=sub.id, price=total_price)

        cartitem.save()
    return HttpResponseRedirect(reverse("cart"))

def add_pasta(request):
    if request.method == "POST":
        print(request.POST)
        pasta_id = request.POST["pasta"] 
        pasta = Pasta.objects.get(pk=pasta_id)

        cartitem = CartItem(item=pasta, user=request.user, item_type="Pasta", item_id=pasta.id, price=pasta.price)
        cartitem.save()

    # TODO Instead of rendering cart, redirect back to user.html menu so user can add more items to cart
    return HttpResponseRedirect(reverse("cart"))


# TODO Fix duplicate with add_pasta
def add_salad(request):
    if request.method == "POST":
        print(request.POST)
        salad_id = request.POST["salad"] 
        salad = Salad.objects.get(pk=salad_id)

        cartitem = CartItem(item=salad, user=request.user, item_type="Salad", item_id=salad.id, price=salad.price)
        cartitem.save()

    # TODO Instead of rendering cart, redirect back to user.html menu so user can add more items to cart
    return HttpResponseRedirect(reverse("cart"))


def add_platter(request):
    if request.method == "POST":
        print(request.POST)
        platter_id = request.POST["dinnerplatter"] 
        platter = DinnerPlatter.objects.get(pk=platter_id)

        cartitem = CartItem(item=platter, user=request.user, item_type="DinnerPlatter", item_id=platter.id, price=platter.price)
        cartitem.save()

    # TODO Instead of rendering cart, redirect back to user.html menu so user can add more items to cart
    return HttpResponseRedirect(reverse("cart"))


def order(request):
    # Submit the order once user confirms cart items and price    
    # Query for all of user's cart items
    cart_items = CartItem.objects.filter(user=request.user)

    # Dict to map item type to matching Class
    d = {"Pizza": Pizza, "Sub": Sub, "Pasta": Pasta, "Salad": Salad, "DinnerPlatter": DinnerPlatter, "Addition": Addition, "Topping": Topping}
    for item in cart_items:
        i_type = item.item_type
        i_id = item.item_id

        # Query for the particular item from the relevant table
        # Add the user's order for that item
        obj = d[i_type].objects.get(pk=i_id)
        print(obj)
        obj.user.add(request.user)
        print("SUCCESS")

    # Delete all of user's cart items
    cart_items.delete()

    # Redirect user to menu page
    return render(request, "orders/cart.html", {
        "success": True
    })


def view_orders(request):
    if request.user.is_superuser:
        all_users = User.objects.all()
        all_orders = {}

        for u in all_users:
            user_orders = []

            if u.pizza_orders.all(): 
                [user_orders.append(o) for o in u.pizza_orders.all()]
                if u.topping_orders.all():
                    [user_orders.append(o) for o in u.topping_orders.all()]

            if u.sub_orders.all(): 
                [user_orders.append(o) for o in u.sub_orders.all()]
                if u.addn_orders.all():
                    [user_orders.append(o) for o in u.addn_orders.all()]

            if u.pasta_orders.all(): 
                [user_orders.append(o) for o in u.pasta_orders.all()]

            if u.salad_orders.all(): 
                [user_orders.append(o) for o in u.salad_orders.all()]

            if u.plat_orders.all(): 
                [user_orders.append(o) for o in u.plat_orders.all()]

            all_orders[u] = user_orders

        # Query for all items' orders
        return render(request, "orders/allorders.html", {
            "all_orders": all_orders.items()
        })
    else:
        return HttpResponseRedirect(reverse("index"))