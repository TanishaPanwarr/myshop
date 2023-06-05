from django.contrib import admin

from products.models import Category, Product ,Article

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Article)