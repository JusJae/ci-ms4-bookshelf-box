from django import forms
from .models import SubscriptionOption


class SubscriptionOptionForm(forms.ModelForm):
    BOOK_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
    )

    number_of_books = forms.ChoiceField(
        choices=BOOK_CHOICES,
        widget=forms.RadioSelect,
        label="Number of Books",
        initial='1'
    )

    class Meta:
        model = SubscriptionOption
        fields = ['category', 'number_of_books', 'subscription_type']

    def __init__(self, *args, **kwargs):
        super(SubscriptionOptionForm, self).__init__(*args, **kwargs)

        placeholders = {
            'category': 'Select Category',
            'subscription_type': 'Select Subscription Type',
        }

        self.fields['category'].widget = forms.Select(
            choices=[('', placeholders['category'])] +
            list(self.fields['category'].choices)[1:],
            attrs={'class': 'form-control text-center'}
        )
        self.fields['subscription_type'].widget = forms.Select(
            choices=[('', placeholders['subscription_type'])] +
            list(self.fields['subscription_type'].choices)[1:],
            attrs={'class': 'form-control text-center'}
        )
