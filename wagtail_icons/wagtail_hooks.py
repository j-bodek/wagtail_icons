from django.urls import path, reverse, include

from wagtail.admin.menu import MenuItem
from wagtail.core import hooks

from wagtail_icons import admin_urls

# register url
@hooks.register('register_admin_urls')
def register_icons_url():
    return [
        path('icons/', include(admin_urls, namespace='wagtailicons')),
    ]

# register menu item
@hooks.register('register_admin_menu_item')
def register_icons_menu_item():
    return MenuItem('Icons', reverse('wagtailicons:index'), icon_name='tick-inverse', order=400)