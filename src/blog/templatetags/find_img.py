from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def get_first_image_tag(data):
    if '![](data:image/' in data:
        data = data.replace('![]', '')
        
        start_index = data.find("(data:image")
        end_index = data.find(")", start_index)

        data = f'<img src="{data[start_index + 1:end_index]}">'
        
        return mark_safe(data)
    
    else:
        return None