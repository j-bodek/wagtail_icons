
import weakref
from django import template
from django.template.defaulttags import register
import re
from django.utils.safestring import mark_safe

register = template.Library()

@register.inclusion_tag('wagtail_icons/templatetags/icon.html')
def icon(icon, size=None, class_name=None, color=None):
    with open(icon.file.path, 'r') as f:
        content = f.read()
        content = str(content)
        content = re.sub('[\t\n]+', ' ', content)
        svg = re.search(r'<svg(.*?)>(.*)<\/svg>', content)
        svg_parameters = svg.group(1)
        svg_content = svg.group(2)
        
        if size:
            svg_parameters = resize_icon(svg_parameters, size)
        if class_name:
            svg_parameters = add_new_class(svg_parameters, class_name)
        if color:
            svg_parameters, svg_content = change_svg_color(svg_parameters, svg_content, color)

    return{
        'svg_parameters':mark_safe(svg_parameters),
        'svg_content':mark_safe(svg_content)
    }

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

def change_svg_color(svg_parameters, svg_content, color):
    fill_parameter_found = False
    # modify fill parameter for path
    if re.search(r'fill="([#0-9a-zA-Z]*)"', svg_content):
        fill_parameter_found = True
        svg_content = re.sub(r'fill="([#0-9a-zA-Z]*)"', f'fill="{str(color)}"', svg_content)
    if re.search(r'fill:([#0-9a-zA-Z]*)', svg_content):
        fill_parameter_found = True
        svg_content = re.sub(r'fill:([#0-9a-zA-Z]*)', f'fill:{str(color)}', svg_content)

    # modify fill parameter for svg element
    if re.search(r'fill="([#0-9a-zA-Z]*)"', svg_parameters):
        fill_parameter_found = True
        svg_parameters = re.sub(r'fill="([#0-9a-zA-Z]*)"', f'fill="{str(color)}"', svg_parameters)
    if re.search(r'fill:([#0-9a-zA-Z]*)', svg_parameters):
        fill_parameter_found = True
        svg_parameters = re.sub(r'fill:([#0-9a-zA-Z]*)', f'fill:{str(color)}', svg_parameters)

    # if fill parameter is not found
    if not fill_parameter_found:
        svg_parameters += f' fill="{str(color)}"'
    return svg_parameters, svg_content

def resize_icon(svg_parameters, size):
    height, width = size.split('x')
    if not re.search(r'height="([0-9a-z ]*)"', svg_parameters):
        svg_parameters += f' height="{str(height)}"'
    else:
        svg_parameters = re.sub(r'height="([0-9a-z ]*)"', f'height="{str(height)}"', svg_parameters)

    if not re.search(r'width="([0-9a-z ]*)"', svg_parameters):
        svg_parameters += f' width="{str(width)}"'
    else:
        svg_parameters = re.sub(r'width="([0-9a-z ]*)"', f'width="{str(width)}"', svg_parameters)
        
    return svg_parameters

def add_new_class(svg_parameters, class_name):
    if not re.search(r'class=".*?"', svg_parameters):
        svg_parameters = f'class="{class_name}" {svg_parameters}'
    else:
        classes = re.search(r'class="(.*?)"', svg_parameters).group(1)
        svg_parameters = re.sub(r'class=".*?"', f'class="{classes} {class_name}"', svg_parameters)

    return svg_parameters