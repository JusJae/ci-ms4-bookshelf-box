from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Mapping from string numbers to integers
string_to_number = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5,
}


@register.filter(name='stars')
def string_to_stars(value):
    if value is None:
        return ''  # Return an empty string if value is None
    try:
        value = int(value)  # Convert the value to an integer
    except (ValueError, TypeError):
        # Log the error or handle it appropriately
        return ''  # Return an empty string in case of error
    return mark_safe('<i class="fa-solid fa-star"></i>' * value)
