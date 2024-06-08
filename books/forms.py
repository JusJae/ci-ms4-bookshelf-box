from django import forms
from .models import Book, Category
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            'title',
            'category',
            'image_url',
            'rating',
            'description',
            'upc',
            'price',
            'reviews',
            Submit('submit', 'Save', css_class='btn btn-primary')
        )


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
