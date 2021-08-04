from django.urls import path
from . import views


app_name = 'listings'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:section_slug>', views.product_list, name='product_list_by_section'),
    path('<slug:section_slug>/<slug:product_slug>', views.product_detail, name='product_detail'),
]
