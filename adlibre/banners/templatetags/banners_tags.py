from django import template

from adlibre.banners.models import Banner

register = template.Library()

@register.inclusion_tag('banners/banners_list.html')
def images_list(banner_id = 'default'):
    """
    First loading banner from CMS.
    If none provided loading a banner with name 'default'.
    Templatetag raises a value error in case banner with name 'default' does not exist.
    !!! So make sure there is one !!!
    
    Then returns a slideshow of banner instance to provided template.
    """
    banner = []
    try:
        banner = Banner.objects.get(name=banner_id)
    except:
        pass
    if banner == [] and banner_id == 'default':
        raise ValueError('No default banner added in admin. Please add at least one banner with name "default"')
    return {'banner': banner,}
