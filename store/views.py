from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Product, Cart, CartItem, Order, OrderItem
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, product_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return JsonResponse({'message': 'Item added to cart'})

@login_required
def remove_from_cart(request, product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.delete()
    return JsonResponse({'message': 'Item removed from cart'})

@login_required
def view_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    items = [{'product': item.product.name, 'quantity': item.quantity, 'price': item.product.price} for item in cart_items]
    return JsonResponse({'cart_items': items})

@login_required
def place_order(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    if not cart_items:
        return JsonResponse({'message': 'Cart is empty'}, status=400)

    order = Order.objects.create(user=request.user, total_price=sum(item.product.price * item.quantity for item in cart_items))
    
    for item in cart_items:
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
    
    cart_items.delete()  # Clear the cart
    return JsonResponse({'message': 'Order placed successfully'})

