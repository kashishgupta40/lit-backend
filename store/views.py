from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Product, Cart, CartItem, Order, OrderItem
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound


# Traditional Django views (for rendering web pages)
@login_required
def add_to_cart(request, product_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return Response({'message': 'Item added to cart'})


@login_required
def remove_from_cart(request, product_id):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.delete()
        return Response({'message': 'Item removed from cart'})
    except Cart.DoesNotExist:
        raise NotFound(detail="Cart not found")
    except CartItem.DoesNotExist:
        raise NotFound(detail="Product not found in cart")


@login_required
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        items = [{'product': item.product.name, 'quantity': item.quantity, 'price': item.product.price} for item in cart_items]
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return Response({'cart_items': items, 'total_price': total_price})
    except Cart.DoesNotExist:
        raise NotFound(detail="Cart not found")


@login_required
def place_order(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        
        if not cart_items:
            return Response({'message': 'Cart is empty'}, status=400)

        total_price = sum(item.product.price * item.quantity for item in cart_items)
        order = Order.objects.create(user=request.user, total_price=total_price)
        
        order_items = []
        for item in cart_items:
            order_items.append(OrderItem(order=order, product=item.product, quantity=item.quantity, price=item.product.price))
        
        OrderItem.objects.bulk_create(order_items)  # Insert all order items in bulk
        
        cart_items.delete()  # Clear the cart after placing the order
        
        return Response({'message': 'Order placed successfully'})
    except Cart.DoesNotExist:
        return Response({'message': 'Cart not found'}, status=404)


# Django REST Framework API views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_add_to_cart(request, product_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return Response({'message': 'Item added to cart'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_remove_from_cart(request, product_id):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.delete()
        return Response({'message': 'Item removed from cart'})
    except Cart.DoesNotExist:
        raise NotFound(detail="Cart not found")
    except CartItem.DoesNotExist:
        raise NotFound(detail="Product not found in cart")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        items = [{'product': item.product.name, 'quantity': item.quantity, 'price': item.product.price} for item in cart_items]
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return Response({'cart_items': items, 'total_price': total_price})
    except Cart.DoesNotExist:
        raise NotFound(detail="Cart not found")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_place_order(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        
        if not cart_items:
            return Response({'message': 'Cart is empty'}, status=400)
        
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        order = Order.objects.create(user=request.user, total_price=total_price)
        
        order_items = []
        for item in cart_items:
            order_items.append(OrderItem(order=order, product=item.product, quantity=item.quantity, price=item.product.price))
        
        OrderItem.objects.bulk_create(order_items)  # Insert all order items in bulk
        
        cart_items.delete()  # Clear the cart after placing the order
        
        return Response({'message': 'Order placed successfully'})
    except Cart.DoesNotExist:
        return Response({'message': 'Cart not found'}, status=404)
