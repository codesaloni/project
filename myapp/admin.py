from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import CustomUser,Product,CartItem

class UserAdmin(DefaultUserAdmin):
    model = CustomUser
    # Define the fields to be used in the User creation and change forms.
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type'),
        }),
    )
    list_display = ('username', 'email', 'user_type', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)

# Register the CustomUser model with the customized UserAdmin
admin.site.register(CustomUser, UserAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image' )

admin.site.register(Product, ProductAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display=('id','user','product','quantity')

admin.site.register(CartItem,CartAdmin)
