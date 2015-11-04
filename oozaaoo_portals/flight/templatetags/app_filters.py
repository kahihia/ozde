from django import template
from flight.models import Iata
register = template.Library()

@register.filter
def get_range(value):
    value = int(value)
    return range( value )

@register.filter
def airport(code):
    value = '  '+code
    airport_name = Iata.objects.get(code=value)
    return airport_name.airportname
