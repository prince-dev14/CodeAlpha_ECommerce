from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CheckoutForm
from .models import Order, OrderItem, Product


def product_list(request):
    q = request.GET.get('q', '').strip()
    products = Product.objects.all()
    if q:
        products = products.filter(name__icontains=q)
    return render(request, 'shop/product_list.html', {'products': products, 'q': q})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})


def _cart_items(request):
    cart = request.session.get('cart', {})
    items, total = [], 0
    for pid, qty in cart.items():
        product = Product.objects.filter(pk=pid).first()
        if not product:
            continue
        subtotal = product.price * qty
        total += subtotal
        items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})
    return items, total


def cart_view(request):
    items, total = _cart_items(request)
    return render(request, 'shop/cart.html', {'items': items, 'total': total})


@require_POST
def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    try:
        qty = max(int(request.POST.get('quantity', 1)), 1)
    except ValueError:
        qty = 1
    cart = request.session.get('cart', {})
    new_qty = cart.get(str(pk), 0) + qty
    if product.stock <= 0:
        messages.error(request, f'{product.name} is out of stock.')
        return redirect('product_detail', pk=pk)
    if new_qty > product.stock:
        new_qty = product.stock
        messages.warning(request, f'Only {product.stock} of {product.name} available.')
    else:
        messages.success(request, f'Added {product.name} to your cart.')
    cart[str(pk)] = new_qty
    request.session['cart'] = cart
    return redirect('cart')


@require_POST
def cart_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})
    try:
        qty = int(request.POST.get('quantity', 1))
    except ValueError:
        qty = 1
    if qty <= 0:
        cart.pop(str(pk), None)
    else:
        cart[str(pk)] = min(qty, product.stock)
    request.session['cart'] = cart
    return redirect('cart')


@require_POST
def cart_remove(request, pk):
    cart = request.session.get('cart', {})
    cart.pop(str(pk), None)
    request.session['cart'] = cart
    return redirect('cart')


@login_required
def checkout(request):
    items, total = _cart_items(request)
    if not items:
        messages.info(request, 'Your cart is empty.')
        return redirect('product_list')
    form = CheckoutForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                address=form.cleaned_data['address'],
                total=total,
            )
            for it in items:
                p = Product.objects.select_for_update().get(pk=it['product'].pk)
                qty = min(it['quantity'], p.stock)
                if qty <= 0:
                    continue
                OrderItem.objects.create(order=order, product=p, name=p.name, price=p.price, quantity=qty)
                p.stock -= qty
                p.save()
        request.session['cart'] = {}
        messages.success(request, f'Order #{order.pk} placed successfully!')
        return redirect('order_list')
    return render(request, 'shop/checkout.html', {'form': form, 'items': items, 'total': total})


@login_required
def order_list(request):
    orders = request.user.orders.prefetch_related('items')
    return render(request, 'shop/order_list.html', {'orders': orders})


def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Welcome! Your account has been created.')
        return redirect('product_list')
    return render(request, 'registration/register.html', {'form': form})
