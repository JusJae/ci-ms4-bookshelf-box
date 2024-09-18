from django import template

register = template.Library()


@register.filter(name='bootstrap_class')
def bootstrap_class(message_tag):
    bootstrap_classes = {
        'error': 'danger',
        'debug': 'secondary',
        'info': 'info',
        'success': 'success',
        'warning': 'warning',
    }
    return bootstrap_classes.get(message_tag, 'info')
