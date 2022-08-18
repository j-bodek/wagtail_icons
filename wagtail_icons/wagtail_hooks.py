from django.urls import path, reverse, include

from wagtail.admin.menu import MenuItem

try:
    from wagtail import hooks
except ImportError:
    from wagtail.core import hooks

from wagtail_icons import admin_urls
from wagtail_icons.views.chooser import IconsChooserViewSet

# register url
@hooks.register('register_admin_urls')
def register_icons_url():
    return [
        path('icons/', include(admin_urls, namespace='wagtailicons')),
    ]

@hooks.register('register_admin_viewset')
def register_person_chooser_viewset():
    return IconsChooserViewSet('wagtailicons_modal', url_prefix='wagtailicons-modal')

# register menu item
@hooks.register('register_admin_menu_item')
def register_icons_menu_item():
    return MenuItem('Icons', reverse('wagtailicons:index'), icon_name='tick-inverse', order=400)