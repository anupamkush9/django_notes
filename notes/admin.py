from django.contrib import admin
from .models import *

class BookAdmin(admin.ModelAdmin):
    list_display = ['photo', 'book_name']

class FilesAdmin(admin.ModelAdmin):
        class Media:
            js = (
                'https://code.jquery.com/jquery-3.6.1.min.js',
                'js/FilesAdmin.js',  # project static folder
            )

# Register your models here
admin.site.register(Files, FilesAdmin)
admin.site.register(Temp_Data_Bulk_Create)
admin.site.register(Book, BookAdmin)
