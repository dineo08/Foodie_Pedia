from django.contrib import admin
from .models import *



# Register your models here.
admin.site.register(Profile)
admin.site.register(Recipe)
admin.site.register(User_Ingredient)
admin.site.register(Ingredient)
admin.site.register(Recipe_Ingredients)
admin.site.register(Favourite_Recipe)
