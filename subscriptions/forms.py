from django import forms
from books.models import Category
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, Field


class SubscriptionOptionForm(forms.Form):
    PLAN_CHOICES = [
        ('basic', 'Basic £9.99 for 3 books'),
        ('standard', 'Standard £19.99 for 5 books'),
        ('premium', 'Premium £29.99 for 7 books'),
    ]

    plan = forms.ChoiceField(
        choices=PLAN_CHOICES,
        widget=forms.RadioSelect,
        label="",
        initial='basic'
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    subscription_type = forms.ChoiceField(
        choices=[('one-off', 'One-off'), ('monthly', 'Monthly'),
                 ('every_3_months', 'Every 3 months')],
        widget=forms.RadioSelect,
        initial='one-off'
    )

    def __init__(self, *args, **kwargs):
        super(SubscriptionOptionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Choose a plan',
                Div('plan', css_class='choices-group'),
                css_class='form-group'
            ),
            Fieldset(
                'Select Book Categories',
                'categories',
                css_class='form-group'
            ),
            Fieldset(
                'Choose Subscription Type',
                'subscription_type',
                css_class='form-group'
            ),
        )
