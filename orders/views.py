from django.shortcuts import render, redirect
from django.contrib import messages
from cart.views import _get_cart
from weather.services import get_weather
from .models import Order, OrderItem


def checkout(request):
    if request.method == 'POST':
        cart = _get_cart(request)
        items = cart.items.all()
        if not items:
            messages.error(request, 'Корзина пуста')
            return redirect('catalog:product_list')

        city = request.POST.get('city', '')
        weather = get_weather(city) if city else None

        order = Order.objects.create(
            customer_name=request.POST.get('name', ''),
            address=request.POST.get('address', ''),
            city=city,
            weather_info=str(weather) if weather else '',
        )
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
            if item.product.stock >= item.quantity:
                item.product._update_stock(item.quantity)
        cart.delete()
        return render(request, 'orders/success.html', {'order': order})

    cart = _get_cart(request)
    return render(request, 'orders/checkout.html', {'cart': cart})