from django.shortcuts import render, get_object_or_404
from .models import Section, Product
from cart.forms import CartAddProductForm


def product_list(request, section_slug=None):
    sections = Section.objects.all()
    if section_slug:
        requested_section = get_object_or_404(Section, slug=section_slug)
        products = Product.objects.filter(section=requested_section)
    else:
        requested_section = None
        products = Product.objects.all()
    return render(request,
                  'product/list.html',
                  {'sections': sections,
                   'requested_section': requested_section,
                   'products': products,
                   'main_shop_page': True})


def product_detail(request, section_slug, product_slug):
    section = get_object_or_404(Section, slug=section_slug)
    product = get_object_or_404(Product, section_id=section.id, slug=product_slug)

    cart_product_form = CartAddProductForm()
    return render(request,
                  'product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})
