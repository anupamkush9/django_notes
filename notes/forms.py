from django import forms
from .models import Book

class Bookform(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'