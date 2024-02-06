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


# @register.filter(name='stars')
# def string_to_stars(value):
#     print(f"Converting value: {value}")
#     # Convert the string number to an integer
#     number = string_to_number.get(value.lower(), 0)
#     # Return that number of stars as FA icon
#     stars_html = ''.join(
#         ['<i class="fa-solid fa-star"></i>' for _ in range(number)])
#     return mark_safe(stars_html)
#     # mark safe tells django not to escape html


# @register.filter(name='test_stars')
# def test_stars(value):
#     return "✩✩✩✩✩"


@register.filter(name='stars')
def string_to_stars(value):
    # Simplified filter logic for demonstration
    return mark_safe('<i class="fa-solid fa-star"></i>' * int(value))
