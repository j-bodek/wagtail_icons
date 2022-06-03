
from django import template
from django.template.defaulttags import register
import re

register = template.Library()



@register.filter()
def add_url_parameter(path, parameter):
    try:
        main_path, path_parameters = path.split('?', 1)
        path_parameters = {p.split("=")[0]:p.split("=")[1] for p in path_parameters.split("&")}
        parameter_key, parameter_value = parameter.split('=', 1)
        if parameter_key in path_parameters.keys():
            path_parameters = '&'.join([f"{k}={v}" if k != parameter_key else parameter for k,v in path_parameters.items()])
            return f"{main_path}?{path_parameters}"
        else:
            return f"{path}&{parameter}"
    except ValueError:
        return f"{path}?{parameter}"