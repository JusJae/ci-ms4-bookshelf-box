from django import forms
from .models import SubscriptionOption


# class SubscriptionOptionForm(forms.ModelForm):
#     class Meta:
#         model = SubscriptionOption
#         fields = ['category', 'number_of_books', 'subscription_type']
#         widgets = {
#             'category': forms.Select(attrs={'class': 'form-control'}),
#             'number_of_books': forms.NumberInput(attrs={'class': 'form-control'}),
#             'subscription_type': forms.Select(attrs={'class': 'form-control'}),
#         }

class SubscriptionOptionForm(forms.ModelForm):
    class Meta:
        model = SubscriptionOption
        fields = ['category', 'number_of_books', 'subscription_type']

    def __init__(self, *args, **kwargs):
        super(SubscriptionOptionForm, self).__init__(*args, **kwargs)

        placeholders = {
            'category': 'Select Category',
            'number_of_books': 'Number of Books',
            'subscription_type': 'Subscription Type',
        }
        # TODO: Add placeholder to the category field as well as titles for each field
        # https://stackoverflow.com/questions/11391308/django-forms-how-to-set-a-placeholder-for-the-first-option-in-a-select-box

        self.fields['category'].widget.attrs['autofocus'] = True
        for field_name, field in self.fields.items():
            if field_name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[field_name]
            field.widget.attrs['class'] = 'form-control border-black rounded my-2'
            field.label = False
