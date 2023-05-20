from django import forms
from .models import Book
from .models import Feedback

class Bookform(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']
        labels = {
            'name': 'Your Name',
            'email': 'Your Email',
            'message': 'Your Message',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter your message'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name == 'danger' or name == '':
            raise forms.ValidationError("Name is not valid.")
        return name

