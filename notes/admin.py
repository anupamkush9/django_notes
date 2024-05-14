from django.contrib import admin
from .models import *
from django import forms
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.http import JsonResponse

class BookAdmin(admin.ModelAdmin):
    list_display = ['photo', 'book_name']
    
    def get_urls(self):
        urls = [
                path('bookprice', login_required(self.get_book_price, login_url="/admin/login/"), name='book_price'),
                path('bookprice_by_id/<int:id>', login_required(self.get_book_price_by_id, login_url="/admin/login/"), name='get_book_price_by_id'),
            ]+super().get_urls()
        return urls

    def get_book_price(self, request):
        price = 12
        return JsonResponse({'price': price})

    def get_book_price_by_id(self, request, id):
        price = int(id)*4
        return JsonResponse({'price': price})


class FilesAdmin(admin.ModelAdmin):
        list_display = ['name', 'url', 'hash_id']
        class Media:
            js = (
                'https://code.jquery.com/jquery-3.6.1.min.js',
                'js/FilesAdmin.js',  # project static folder
            )
            css = (
                  {"all" : ("css/custom_admin.css",),}
            )
# class BookAdmin(admin.ModelAdmin):
#     list_display = ['photo', 'book_name']

class FilesAdmin(admin.ModelAdmin):
        class Media:
            js = (
                'https://code.jquery.com/jquery-3.6.1.min.js',
                'js/FilesAdmin.js',  # project static folder
            )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', ]

class productsAdminForm(forms.ModelForm):
    class Meta:
        model  = Product
        fields = ['name', 'category']
    # we can apply validation by one more way that is django.forms.validators. 
    # it provides most common validation functions like minlength and maxlength, etc.


    # def clean_name(self):
    #     """
    #         1. Example of field level validation in Django.
    #         2. This is used when we want to apply validationo on single field.
    #     """
    #     name = self.cleaned_data.get('name')
    #     if name == 'temp':
    #         raise forms.ValidationError("Hi bro, please Enter a valid name..............")


    def clean(self):
        """
            1. Exmaple of form level validation in Django
            2. This is used when we want to apply validation on complete form.
        """
        name = self.cleaned_data.get('name')
        if name == "faltu":
            raise forms.ValidationError("Hi bro, please Enter a valid name")

class ProductAdmin(admin.ModelAdmin):
    # below we have override the form which is defined in parent class.
    form = productsAdminForm
    list_display = ['name', ]

    # we can override save model method from here by overriding below method.
    # def save_model(self, request, obj, form, change):

# Register your models here
admin.site.register(Files, FilesAdmin)
admin.site.register(Temp_Data_Bulk_Create)
admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Feedback)
admin.site.register(Mobiles)
