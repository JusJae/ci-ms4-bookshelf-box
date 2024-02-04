from django import forms
from books.models import Category
from .models import SubscriptionOption, Book


class SubscriptionOptionForm(forms.ModelForm):
    class Meta:
        model = SubscriptionOption
        fields = ['category', 'number_of_books', 'subscription_type', 'price']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'number_of_books': forms.NumberInput(attrs={'class': 'form-control'}),
            'subscription_type': forms.Select(attrs={'class': 'form-control'}),
        }
