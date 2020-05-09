from django.contrib import admin

from .models import (Size, Pizza, PizzaName, PizzaType, Topping, Addition,
                    Sub, Pasta, Salad, DinnerPlatter, CartItem)


class OrderAdmin(admin.ModelAdmin):
    filter_horizontal = ("user",)

# Register your models here.
admin.site.register(PizzaName)
admin.site.register(Size)
admin.site.register(PizzaType)
admin.site.register(Topping)
admin.site.register(Addition, OrderAdmin)
admin.site.register(Pizza, OrderAdmin)
admin.site.register(Sub, OrderAdmin)
admin.site.register(Pasta, OrderAdmin)
admin.site.register(Salad, OrderAdmin)
admin.site.register(DinnerPlatter, OrderAdmin)
admin.site.register(CartItem)







