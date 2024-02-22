from django.shortcuts import render,redirect,get_object_or_404
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import os
from django.conf import settings
from django.db.models import Sum, F
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'general/index.html', context)


def about_us(request):
    return render(request, 'general/about_us.html')


def contact_us(request):
    return render(request, 'general/contact_us.html')


def shop(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'general/shop.html', context)


def single_product(request,pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product':product}
    return render(request, 'general/single_product.html', context)




# def add_to_cart(request, pk):
#     user = request.user

#     if user.is_authenticated:
#         product = get_object_or_404(Product, pk=pk)
#         quantity = 1  # You can customize this based on your requirements
#         price = product.price

#         # Check if the product is already in the user's cart
#         existing_cart_item = AddToCart.objects.filter(user=user, product=product).first()

#         if existing_cart_item:
#             # If the product is already in the cart, update the quantity
#             existing_cart_item.quantity += quantity
#             existing_cart_item.save()
#         else:
#             # If the product is not in the cart, create a new cart item
#             cart_item = AddToCart(user=user, product=product, quantity=quantity, price=price)
#             cart_item.save()

#         messages.success(request, f"{product.product_name} added to your cart.")
#         return redirect('shop')  # Redirect to the cart page or any other page you want after adding to cart
    


def add_to_cart(request, pk):
    user = request.user

    if user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)

        # Check if the product is in stock
        if product.quantity > 0:
            quantity = 1  # You can customize this based on your requirements
            price = product.price

            # Check if the product is already in the user's cart
            existing_cart_item = AddToCart.objects.filter(user=user, product=product).first()

            if existing_cart_item:
                # If the product is already in the cart, update the quantity
                existing_cart_item.quantity += quantity
                existing_cart_item.save()
            else:
                # If the product is not in the cart, create a new cart item
                cart_item = AddToCart(user=user, product=product, quantity=quantity, price=price)
                cart_item.save()

            messages.success(request, f"{product.product_name} added to your cart.")
        else:
            messages.error(request, f"{product.product_name} is out of stock.")

        return redirect('shop')  # Redirect to the cart page or any other page you want after adding to cart
 

def add_to_cart2(request):
    user = request.user

    if user.is_authenticated:
        if request.method == "POST":
            quantity = int(request.POST.get('quantity'))  # Convert quantity to an integer
            product_id = int(request.POST.get('pid'))  # Convert product ID to an integer

            product_detail = get_object_or_404(Product, pk=product_id)

            price = product_detail.price
            total_price = quantity * price

            existing_cart_item = AddToCart.objects.filter(user=user, product=product_detail).first()

            if existing_cart_item:
                # If the product is already in the cart, update the quantity
                existing_cart_item.quantity += quantity
                existing_cart_item.save()
            else:
                # If the product is not in the cart, create a new cart item
                cart_item = AddToCart(user=user, product=product_detail, quantity=quantity, price=total_price)
                cart_item.save()

            messages.success(request, f"{product_detail.product_name} added to your cart.")
            return redirect('shop')  # Redirect to the cart page or any other page you want after adding to cart

    return redirect('user_log')  # Redirect to the login page if the user is not authenticated



# def cart(request):
#     userid = request.user.pk
#     cart_items = AddToCart.objects.filter(user=userid)

#     for cart_item in cart_items:
#         # Update the single_total for display in the template
#         cart_item.single_total = cart_item.product.price * cart_item.quantity

#         # Update the price field in the AddToCart model based on the current product price and quantity
#         cart_item.price = cart_item.product.price * cart_item.quantity
#         cart_item.save()

#     # Calculate total amounts for each product and subtotal
#     subtotal = cart_items.aggregate(total_price=Sum('price'))['total_price'] or 0
#     shipping_charge = 0
#     total = subtotal + shipping_charge

#     context = {
#         'cart_items': cart_items,
#         'subtotal': subtotal,
#         'shipping_charge': shipping_charge,
#         'total': total,
#     }

#     return render(request, 'general/cart.html', context)


from django.db.models import F

# def cart(request):
#     userid = request.user.pk
#     cart_items = AddToCart.objects.filter(user=userid)

#     for cart_item in cart_items:
#         # Update the single_total for display in the template
#         cart_item.single_total = cart_item.product.price * cart_item.quantity

#         # Update the price field in the AddToCart model based on the current product price and quantity
#         cart_item.price = cart_item.product.price * cart_item.quantity
#         cart_item.save()

#         # Get the available quantity of the product
#         available_quantity = cart_item.product.quantity

#         # Update the cart item to include the available quantity
#         cart_item.product.available_quantity = available_quantity

#     # Calculate total amounts for each product and subtotal
#     subtotal = cart_items.aggregate(total_price=Sum('price'))['total_price'] or 0
#     shipping_charge = 0
#     total = subtotal + shipping_charge

#     context = {
#         'cart_items': cart_items,
#         'subtotal': subtotal,
#         'shipping_charge': shipping_charge,
#         'total': total,
#     }

#     return render(request, 'general/cart.html', context)


# from django.db.models import F, ExpressionWrapper, fields

# def cart(request):
#     userid = request.user.pk
#     cart_items = AddToCart.objects.filter(user=userid)

#     allow_checkout = True  # Initialize allow_checkout as True by default

#     for cart_item in cart_items:
#         # Update the single_total for display in the template
#         cart_item.single_total = cart_item.product.price * cart_item.quantity

#         # Update the price field in the AddToCart model based on the current product price and quantity
#         cart_item.price = cart_item.product.price * cart_item.quantity
#         cart_item.save()

#         # Get the available quantity of the product
#         available_quantity = cart_item.product.quantity

#         # Update the cart item to include the available quantity
#         cart_item.product.available_quantity = available_quantity

#         # Check if the quantity in the cart exceeds the available quantity for any product
#         if cart_item.quantity > available_quantity:
#             allow_checkout = False  # Set allow_checkout to False if any product quantity exceeds available quantity

#     # Calculate total amounts for each product and subtotal
#     subtotal = cart_items.aggregate(total_price=Sum('price'))['total_price'] or 0
#     shipping_charge = 0
#     total = subtotal + shipping_charge

#     context = {
#         'cart_items': cart_items,
#         'subtotal': subtotal,
#         'shipping_charge': shipping_charge,
#         'total': total,
#         'allow_checkout': allow_checkout,  # Pass allow_checkout to the template
#     }

#     return render(request, 'general/cart.html', context)

from django.db.models import Sum
from django.shortcuts import render
from django.contrib import messages

def cart(request):
    userid = request.user.pk
    cart_items = AddToCart.objects.filter(user=userid)

    allow_checkout = True  # Initialize allow_checkout as True by default
    same_shopkeeper = True  # Initialize same_shopkeeper as True by default
    shopkeepers = set()  # Initialize a set to store shopkeepers in the cart

    for cart_item in cart_items:
        # Update the single_total for display in the template
        cart_item.single_total = cart_item.product.price * cart_item.quantity

        # Update the price field in the AddToCart model based on the current product price and quantity
        cart_item.price = cart_item.product.price * cart_item.quantity
        cart_item.save()

        # Get the available quantity of the product
        available_quantity = cart_item.product.quantity

        # Update the cart item to include the available quantity
        cart_item.product.available_quantity = available_quantity

        # Check if the quantity in the cart exceeds the available quantity for any product
        if cart_item.quantity > available_quantity:
            allow_checkout = False  # Set allow_checkout to False if any product quantity exceeds available quantity
            messages.warning(request, f"Adjust quantity for {cart_item.product.product_name}")

        # Add shopkeeper to the set
        shopkeepers.add(cart_item.product.user_id)

    # If there are more than one shopkeeper in the set, set same_shopkeeper to False
    if len(shopkeepers) > 1:
        same_shopkeeper = False
        allow_checkout = False
        messages.warning(request, "Choose products of the same shopkeeper")

    # Calculate total amounts for each product and subtotal
    subtotal = cart_items.aggregate(total_price=Sum('price'))['total_price'] or 0
    shipping_charge = 0
    total = subtotal + shipping_charge

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_charge': shipping_charge,
        'total': total,
        'allow_checkout': allow_checkout,  # Pass allow_checkout to the template
        'same_shopkeeper': same_shopkeeper,  # Pass same_shopkeeper to the template
    }

    return render(request, 'general/cart.html', context)




from django.http import JsonResponse

def update_cart_quantity(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        quantity = request.POST.get('quantity')

        cart_item = AddToCart.objects.get(pk=cart_item_id)
        cart_item.quantity = quantity
        cart_item.save()

        # Recalculate totals
        cart_items = AddToCart.objects.filter(user=request.user.pk)
        subtotal = cart_items.aggregate(total_price=Sum('price'))['total_price'] or 0
        shipping_charge = 0
        total = subtotal + shipping_charge

        return JsonResponse({
            'single_total': cart_item.product.price * int(quantity),
            'subtotal': subtotal,
            'total': total
        })
    else:
        return JsonResponse({'error': 'Invalid request method'})


def product_remove_cart(request, pk):
    product = get_object_or_404(AddToCart, pk=pk)
    product.delete()
    return redirect('cart')


def order_placed(request):
    return render(request, 'general/order_placed.html')


# @login_required
# def checkout(request):
#     if request.method == 'POST':
#         cart_items = AddToCart.objects.filter(user=request.user)

#         subtotal = cart_items.aggregate(total_price=Sum('price'))['total_price'] or 0
#         shipping_charge = 0
#         total = subtotal + shipping_charge

#         address = request.POST.get('address')
#         # location = request.POST.get('location')
#         city = request.POST.get('city')
#         pincode = request.POST.get('pincode')
#         landmark = request.POST.get('landmark')

#         checkout_instance = Checkout.objects.create(
#             user=request.user,
#             total_price=total,
#             address=address,
#             # location=location,
#             city=city,
#             pincode=pincode,
#             landmark=landmark,
#             status='Pending'
#         )

#         for cart_item in cart_items:
#             OrderedProduct.objects.create(
#                 checkout=checkout_instance,
#                 product=cart_item.product,
#                 quantity=cart_item.quantity,
#                 price=cart_item.price
#             )

#         checkout_instance.save()
#         cart_items.delete()

#         return redirect('order_placed')
    
#     else:
#         cart_items = AddToCart.objects.filter(user=request.user)

#         subtotal = cart_items.aggregate(total_price=Sum('price'))['total_price'] or 0
#         shipping_charge = 0 
#         total = subtotal + shipping_charge

#         context = {
#             'cart_items': cart_items,
#             'subtotal': subtotal,
#             'shipping_charge': shipping_charge,
#             'total': total,
#         }

#         return render(request, 'general/checkout.html', context)
from django.db.models import F

# @login_required
# def checkout(request):
#     if request.method == 'POST':
#         cart_items = AddToCart.objects.filter(user=request.user)

#         subtotal = cart_items.aggregate(total_price=Sum('price'))['total_price'] or 0
#         shipping_charge = 0
#         total = subtotal + shipping_charge

#         address = request.POST.get('address')
#         city = request.POST.get('city')
#         pincode = request.POST.get('pincode')
#         landmark = request.POST.get('landmark')
#         from_date = request.POST.get('from_date')
#         to_date = request.POST.get('to_date')
#         msg = request.POST.get('bill')

#         # Create a checkout instance
#         checkout_instance = Checkout.objects.create(
#             user=request.user,
#             total_price=total,
#             address=address,
#             city=city,
#             pincode=pincode,
#             landmark=landmark,
#             status='Pending',
#             from_date = from_date,
#             to_date = to_date,
#             message = msg,
#         )

#         # Create OrderedProduct instances and decrement the quantity in the Product table
#         for cart_item in cart_items:
#             # Create an OrderedProduct instance
#             OrderedProduct.objects.create(
#                 checkout=checkout_instance,
#                 product=cart_item.product,
#                 quantity=cart_item.quantity,
#                 price=cart_item.price
#             )
#             # Decrement the quantity in the Product table by the quantity in the cart
#             Product.objects.filter(pk=cart_item.product.pk).update(quantity=F('quantity') - cart_item.quantity)

#         # Delete cart items after checkout
#         cart_items.delete()

#         return redirect('order_placed')
    
#     else:
#         cart_items = AddToCart.objects.filter(user=request.user)

#         subtotal = cart_items.aggregate(total_price=Sum('price'))['total_price'] or 0
#         shipping_charge = 0 
#         total = subtotal + shipping_charge

#         context = {
#             'cart_items': cart_items,
#             'subtotal': subtotal,
#             'shipping_charge': shipping_charge,
#             'total': total,
#         }

#         return render(request, 'general/checkout.html', context)



from datetime import datetime

# @login_required
# def checkout(request):
#     if request.method == 'POST':
#         cart_items = AddToCart.objects.filter(user=request.user)
        
#         # Calculate subtotal
#         subtotal = cart_items.aggregate(total_price=Sum('price'))['total_price'] or 0

#         shipping_charge = 0

#         # Calculate total based on subtotal and shipping charge
#         total = subtotal + shipping_charge

#         address = request.POST.get('address')
#         city = request.POST.get('city')
#         pincode = request.POST.get('pincode')
#         landmark = request.POST.get('landmark')
#         from_date_str = request.POST.get('from_date')
#         to_date_str = request.POST.get('to_date')
#         msg = request.POST.get('bill')

#         # Convert date strings to datetime objects
#         from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
#         to_date = datetime.strptime(to_date_str, '%Y-%m-%d')

#         # Calculate number of days between from_date and to_date
#         num_days = (to_date - from_date).days

#         # Adjust total based on number of days and product prices
#         total *= num_days  # Assuming total was the daily price of the product

#         # Create a checkout instance
#         checkout_instance = Checkout.objects.create(
#             user=request.user,
#             total_price=total,
#             address=address,
#             city=city,
#             pincode=pincode,
#             landmark=landmark,
#             status='Pending',
#             from_date=from_date,
#             to_date=to_date,
#             message=msg,
#         )

#         # Create OrderedProduct instances and decrement the quantity in the Product table
#         for cart_item in cart_items:
#             # Create an OrderedProduct instance
#             OrderedProduct.objects.create(
#                 checkout=checkout_instance,
#                 product=cart_item.product,
#                 quantity=cart_item.quantity,
#                 price=cart_item.price
#             )
#             # Decrement the quantity in the Product table by the quantity in the cart
#             Product.objects.filter(pk=cart_item.product.pk).update(quantity=F('quantity') - cart_item.quantity)

#         # Delete cart items after checkout
#         cart_items.delete()

#         return render(request, 'general/payment_gateway.html')

#     else:
#         cart_items = AddToCart.objects.filter(user=request.user)

#         subtotal = cart_items.aggregate(total_price=Sum('price'))['total_price'] or 0
#         shipping_charge = 0 
#         total = subtotal + shipping_charge

#         context = {
#             'cart_items': cart_items,
#             'subtotal': subtotal,
#             'shipping_charge': shipping_charge,
#             'total': total,
#         }

#         return render(request, 'general/checkout.html', context)



@login_required
def checkout(request):
    if request.method == 'POST':
        cart_items = AddToCart.objects.filter(user=request.user)
        subtotal = cart_items.aggregate(total_price=Sum('price'))['total_price'] or 0
        shipping_charge = 0
        total = subtotal + shipping_charge

        address = request.POST.get('address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        landmark = request.POST.get('landmark')
        from_date_str = request.POST.get('from_date')
        to_date_str = request.POST.get('to_date')
        msg = request.POST.get('bill')

        from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d')
        num_days = (to_date - from_date).days
        total *= num_days

        checkout_instance = Checkout.objects.create(
            user=request.user,
            total_price=total,
            address=address,
            city=city,
            pincode=pincode,
            landmark=landmark,
            status='Pending',
            from_date=from_date,
            to_date=to_date,
            message=msg,
            bank_name=None,  # Add dummy values initially
            bank_acc_no=None,
            ifsc=None,
            cvv=None,
            paid=False
        )

        request.session['checkout_id'] = checkout_instance.pk  # Store checkout id in session

        return redirect('payment_gateway', pk=checkout_instance.pk)

    else:
        cart_items = AddToCart.objects.filter(user=request.user)
        subtotal = cart_items.aggregate(total_price=Sum('price'))['total_price'] or 0
        shipping_charge = 0 
        total = subtotal + shipping_charge

        context = {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'shipping_charge': shipping_charge,
            'total': total,
        }

        return render(request, 'general/checkout.html', context)


@login_required
def payment_gateway(request, pk):
    checkout_instance = Checkout.objects.get(pk=pk)
    context = {'checkout_instance':checkout_instance}
    if request.method == 'POST':
        # Assuming the form fields are named accordingly
        bank_name = request.POST.get('bank_name')
        bank_acc_no = request.POST.get('bank_acc_no')
        ifsc = request.POST.get('ifsc')
        cvv = request.POST.get('cvv')

        # Update checkout instance with payment details
        checkout_instance.bank_name = bank_name
        checkout_instance.bank_acc_no = bank_acc_no
        checkout_instance.ifsc = ifsc
        checkout_instance.cvv = cvv
        checkout_instance.paid = True
        checkout_instance.save()

        return redirect('order_placed')

    return render(request, 'general/payment_gateway.html',context)


def user_orders(request):
    user = request.user.pk
    orders = Checkout.objects.filter(user = user)
    context = {'ordered_products': orders}
    return render(request, 'user/user_orders.html', context)


def view_products(request, pk):
    products = OrderedProduct.objects.filter(checkout = pk)
    context = {'products': products}
    return render(request, 'user/view_products.html', context)

# def delete_order2(request, pk):
#     product = get_object_or_404(Checkout, pk=pk)
#     product.delete()
#     return redirect('user_orders')

def delete_order2(request, pk):
    order = get_object_or_404(Checkout, pk=pk)
    if order.status != "Delivered":
        # Only restore quantities if the order status is not "Delivered"
        with transaction.atomic():
            # Start a database transaction to ensure atomicity
            ordered_products = order.ordered_products.all()
            for ordered_product in ordered_products:
                product = ordered_product.product
                product.quantity += ordered_product.quantity  # Restore the quantity
                product.save()  # Save the updated product

    order.delete()  # Delete the order
    return redirect('user_orders')



#####################################################################################
#Admin



def spices_home(request):
    return render(request, 'spices_admin/spices_home.html')



def spices_category(request):
    userid= request.user
    categories = Category.objects.filter(user=userid)

    if request.method == "POST":
        category_name = request.POST.get("category")
        image = request.FILES.get("image")
        category = Category(category_name=category_name, image=image, user=userid)
        category.save()
    
    context = {'categories': categories}

    return render(request, 'spices_admin/spices_category.html', context)


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if category.image:
        image_path = os.path.join(settings.MEDIA_ROOT, str(category.image))
        if os.path.exists(image_path):
            os.remove(image_path)

    category.delete()

    return redirect('spices_category')


def edit_category(request, pk):
    get_category = get_object_or_404(Category, pk=pk)
    
    if request.method == "POST":
        new_category_name = request.POST['category_name']
        get_category.category_name = new_category_name
        if 'image' in request.FILES:
            get_category.image = request.FILES['image']
        get_category.save()
        return redirect('spices_category')
    
    context = {
        'get_category': get_category,
    }
    return render(request, 'spices_admin/edit_category.html', context)



def spices_product(request):
    userid= request.user
    if request.method == "POST":
        product_name = request.POST['name']
        category_id = request.POST['category']
        category = Category.objects.get(pk=category_id)
        price = request.POST['price']
        quantity = request.POST['quantity']
        image = request.FILES.get('image')
        description = request.POST['description']
        product_code = request.POST['code'] # You need to implement a function to generate a unique product code

        product = Product(
            product_name=product_name,
            category=category,
            price=price,
            quantity=quantity,
            image=image,
            description=description,
            product_code=product_code,
            user = userid
        )
        product.save()
        return redirect('spices_product')  # Redirect to the product listing page after successful submission

    categories = Category.objects.filter(user=userid)
    products = Product.objects.filter(user = userid)
    context = {'categories': categories, 'products':products}
    return render(request, 'spices_admin/spices_product.html', context)



def edit_product(request, pk):
    get_product = get_object_or_404(Product, pk=pk)
    all_categories = Category.objects.all()
    
    if request.method == "POST":
        new_product_name = request.POST['product_name']
        new_price = request.POST['price']
        new_quantity = request.POST['quantity']
        new_description = request.POST['description']
        new_category_id = request.POST['category']

        get_product.product_name = new_product_name
        get_product.price = new_price
        get_product.quantity = new_quantity
        get_product.description = new_description
        get_product.category = Category.objects.get(id=new_category_id)

        if 'image' in request.FILES:
            get_product.image = request.FILES['image']

        get_product.save()
        return redirect('spices_product')
    
    context = {
        'get_category': get_product,
        'all_categories': all_categories,
    }
    return render(request, 'spices_admin/edit_product.html', context)


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.image:
        image_path = os.path.join(settings.MEDIA_ROOT, str(product.image))
        
        if os.path.exists(image_path):
            os.remove(image_path)

    product.delete()
    return redirect('spices_product')



# def spices_orders(request):
#     orders = Checkout.objects.all()
#     context = {"orders":orders}
#     return render(request, 'spices_admin/spices_orders.html', context)
@login_required
def spices_orders(request):
    # Filter orders based on the products owned by the logged-in shopkeeper
    shop_keeper_id = request.user.id
    orders = Checkout.objects.filter(ordered_products__product__user_id=shop_keeper_id)
    context = {"orders": orders}
    return render(request, 'spices_admin/spices_orders.html', context)

def view_order_products(request, pk):
    products = OrderedProduct.objects.filter(checkout = pk)
    context = {'products': products}
    return render(request, 'spices_admin/view_order_products.html', context)


# def update_order(request, pk):
#     get_order = get_object_or_404(Checkout, pk=pk)
#     if request.method == "POST":
#         new_status = request.POST['task']
#         new_from_date = request.POST['from_date']
#         new_to_date = request.POST['to_date']

#         get_order.status = new_status
#         get_order.from_date = new_from_date
#         get_order.to_date = new_to_date

#         get_order.save()
#         return redirect('spices_orders')
#     else:
#         context = {
#             'get_order':get_order,
#         }
#         return render(request, 'spices_admin/update_order.html', context)

from datetime import datetime


def update_order(request, pk):
    get_order = get_object_or_404(Checkout, pk=pk)
    if request.method == "POST":
        new_status = request.POST['task']
        new_from_date_str = request.POST['from_date']
        new_to_date_str = request.POST['to_date']

        # Convert string dates to datetime objects
        if new_from_date_str:
            new_from_date = datetime.strptime(new_from_date_str, '%Y-%m-%d').date()
        else:
            new_from_date = get_order.from_date
        
        if new_to_date_str:
            new_to_date = datetime.strptime(new_to_date_str, '%Y-%m-%d').date()
        else:
            new_to_date = get_order.to_date

        get_order.status = new_status
        get_order.from_date = new_from_date
        get_order.to_date = new_to_date

        get_order.save()
        return redirect('spices_orders')
    else:
        context = {
            'get_order': get_order,
        }
        return render(request, 'spices_admin/update_order.html', context)



# def delete_order(request, pk):
#     product = get_object_or_404(Checkout, pk=pk)
#     product.delete()
#     return redirect('spices_orders')


from django.db import transaction

def delete_order(request, pk):
    order = get_object_or_404(Checkout, pk=pk)
    if order.status != "Delivered":
        # Only restore quantities if the order status is not "Delivered"
        with transaction.atomic():
            # Start a database transaction to ensure atomicity
            ordered_products = order.ordered_products.all()
            for ordered_product in ordered_products:
                product = ordered_product.product
                product.quantity += ordered_product.quantity  # Restore the quantity
                product.save()  # Save the updated product

    order.delete()  # Delete the order
    return redirect('spices_orders')



def customer_details(request):
    customers = User.objects.filter(is_customer=True)
    context = {'customers':customers}
    return render(request, 'spices_admin/customer_details.html', context)



def SignOut2(request):
     logout(request)
     return redirect('index')


##################################################################



# def user_reg(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         passw = request.POST.get("pass")
#         if User.objects.filter(email=email).exists():
#             messages.error(request, 'Email already exists')
#             return render(request, 'user/user_reg.html')
#         else:
#             user = User.objects.create_user(
#                 name = name,
#                 username = email,
#                 email = email,
#                 password=passw,
#                 is_customer=True,
#             )
#             # Add a success message
#             messages.success(request, 'Registration successful. You can now log in.')
#             return redirect('user_reg')
#     else:
#         return render(request, 'user/user_reg.html')


# def user_log(request):
#     if request.method == 'POST':
#         uname = request.POST.get('email')
#         passw = request.POST.get('pass')

#         user = User.objects.filter(username=uname).first()
        
#         if user is not None and user.check_password(passw) and user.is_customer:
#             login(request, user)
#             return redirect('index')
#         else:
#             messages.error(request, 'Invalid login credentials.')

#     return render(request, 'user/user_log.html')


def user_reg(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        passw = request.POST.get("pass")
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'user/user_reg.html')
        else:
            user = User.objects.create_user(
                username=email,
                email=email,
                name = name,
                password=passw,
                is_customer=True,
            )
            # Automatically log in the user after registration
            login(request, user)
            # Add a success message
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('index')
    else:
        return render(request, 'user/user_reg.html')


def user_log(request):
    if request.method == 'POST':
        uname = request.POST.get('email')
        passw = request.POST.get('pass')

        user = User.objects.filter(username=uname).first()
        
        if user is not None and user.check_password(passw) and user.is_customer:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'user/user_log.html')





def user_profile(request):
    user = request.user
    if request.method == "POST":
        # Collect form data
        name = request.POST.get('name')
        mobile_number = request.POST.get('mobile_number')
        # location = request.POST.get('location')
        address = request.POST.get('address')
        city = request.POST.get('city')
        landmark = request.POST.get('landmark')
        pincode = request.POST.get('pincode')

        # Update user profile
        user.name = name
        user.mobile_number = mobile_number
        # user.location = location
        user.address = address
        user.city = city
        user.landmark = landmark
        user.pincode = pincode
        user.save()

        return redirect('user_profile')  # Redirect to the same page after update

    return render(request, 'user/user_profile.html', {'user': user})

def SignOut(request):
     logout(request)
     return redirect('index')





def shop_register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        passw = request.POST.get("pass")
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'shop/shop_register.html')
        else:
            user = User.objects.create_user(
                username=email,
                email=email,
                name = name,
                password=passw,
                is_shop=True,
            )
        
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('shop_register')
    else:
        return render(request, 'shop/shop_register.html')
    



def shop_login(request):
    if request.method == 'POST':
        uname = request.POST.get('email')
        passw = request.POST.get('pass')

        user = User.objects.filter(username=uname).first()
        
        if user is not None and user.check_password(passw) and user.is_shop:
            login(request, user)
            return redirect('spices_home')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'shop/shop_login.html')


# def cu_update_order(request, pk):
#     get_order = get_object_or_404(Checkout, pk=pk)
#     if request.method == "POST":
#         new_status = request.POST['task']
#         new_from_date_str = request.POST['from_date']
#         new_to_date_str = request.POST['to_date']

#         # Convert string dates to datetime objects
#         if new_from_date_str:
#             new_from_date = datetime.strptime(new_from_date_str, '%Y-%m-%d').date()
#         else:
#             new_from_date = get_order.from_date
        
#         if new_to_date_str:
#             new_to_date = datetime.strptime(new_to_date_str, '%Y-%m-%d').date()
#         else:
#             new_to_date = get_order.to_date

#         get_order.status = new_status
#         get_order.from_date = new_from_date
#         get_order.to_date = new_to_date

#         get_order.save()
#         return render(request, 'user/user_orders.html')
#     else:
#         context = {
#             'get_order': get_order,
#         }
#         return render(request, 'user/cu_update_order.html', context)