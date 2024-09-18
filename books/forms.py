from django import forms
from .models import Book, Category
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        layout = Layout(
            'title',
            'category',
            'image_url',
            'rating',
            'description',
            Submit('submit', 'Save', css_class='btn btn-primary')
        )
        #  if user and (user.is_superuser or user_has_made_purchase):
            #  layout.append('reviews')

        if user and user.is_superuser:
            layout = Layout(
                'title',
                'category',
                'image_url',
                'rating',
                'description',
                'upc',
                'price',
                'availability',
                'reviews',
                Submit('submit', 'Save', css_class='btn btn-primary')
            )

        self.helper.layout = layout

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise ValidationError('Title must be at least 3 characters long.')
        return title

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price < 0:
            raise ValidationError('Price cannot be negative.')
        return price

    def clean_availability(self):
        availability = self.cleaned_data.get('availability')
        if availability is None or availability < 0:
            raise ValidationError('Availability cannot be negative.')
        return availability


class StockForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['availability']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            'availability',
            Submit('submit', 'Update Stock', css_class='btn btn-primary')
        )

    def clean_availability(self):
        availability = self.cleaned_data.get('availability')
        if availability is None or availability < 0:
            raise ValidationError('Availability cannot be negative.')
        return availability
