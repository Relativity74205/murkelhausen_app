from datetime import date

from django import template

register = template.Library()


@register.filter
def js_date(d: date, *args, **kwargs) -> str:
    """Converts a date object to a JavaScript date string."""
    return f"Date.UTC({d.year}, {d.month - 1}, {d.day})"
