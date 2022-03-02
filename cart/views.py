from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from cart.cart import Cart
from cart.forms import CartAddProductForm
from comics_site.models import Comic


@require_POST
def cart_add(request, comics_id):
    cart = Cart(request)
    comics = get_object_or_404(Comic, id=comics_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(comics=comics,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'], )
    return redirect('cart:cart_detail')


def cart_remove(request, comics_id):
    cart = Cart(request)
    comics = get_object_or_404(Comic, id=comics_id)
    cart.remove(comics)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})
