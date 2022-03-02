from django.shortcuts import render, get_object_or_404

from cart.forms import CartAddProductForm
from comics_site.models import Category, Comic


# def products_list(request, category_slug=None):
#     category = None
#     categories = Category.objects.all()
#     product = Product.objects.filter(avaliable=True)
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         product = product.filter(category=category)
#     return render(request,
#                   'comics_site/list.html',
#                   {'category': category,
#                    'categories': categories,
#                    'product': product})


def comics_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    comics = Comic.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        comics = comics.filter(category=category)
    return render(request,
                  'comics_site/comics/list.html',
                  {'category': category,
                   'categories': categories,
                   'comics': comics,
                   })


# def product_detail(request, id, slug):
#     products = get_object_or_404(
#         Product,
#         id,
#         slug=slug,
#         available=True
#     )
#     return render(request, 'comics_site/detail.html',
#                   {'products': products})


def comics_detail(request, id, slug):
    comics = get_object_or_404(
        Comic,
        id=id,
        slug=slug,
        available=True,
    )
    cart_comics_form = CartAddProductForm()
    return render(request, 'comics_site/comics/detail.html',
                  {'comics': comics,
                   'cart_comics_form': cart_comics_form}
                  )
