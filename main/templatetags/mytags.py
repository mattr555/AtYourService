from django import template

register = template.Library()

@register.filter
def get_range(value):
    """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
    """
    return range(value)

@register.filter
def mult(value, arg):
    "Multiplies the arg and the value"
    return int(value) * int(arg)

@register.filter
def sub(value, arg):
    "Subtracts the arg from the value"
    return int(value) - int(arg)

@register.filter
def div(value, arg):
    "Divides the value by the arg"
    return int(value) / int(arg)

@register.filter
def mod(value, arg):
    return int(value) % int(arg)

@register.filter
def int_div(value, arg):
    return int(value) // int(arg)

def callMethod(obj, methodName):
    method = getattr(obj, methodName)

    if "__callArg" in obj.__dict__:
        ret = method(*obj.__callArg)
        del obj.__callArg
        return ret
    return method()

def args(obj, arg):
    if "__callArg" not in obj.__dict__:
        obj.__callArg = []

    obj.__callArg += [arg]
    return obj

register.filter("call", callMethod)
register.filter("args", args)

@register.filter
def is_org_admin(u):
    return u.groups.filter(name="Org_Admin").count() > 0

@register.filter
def is_volunteer(u):
    return u.groups.filter(name="Volunteer").count() > 0

@register.filter
def date_value(date):
    return date.strftime('%m/%d/%Y %I:%M %p')
