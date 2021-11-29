from django.contrib import admin

# Register your models here.

from .models import Book, Category, Order, OrderItem, Review, ShippingAddress, Writer

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Writer)
admin.site.register(Review)
# new
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
