from django.urls import path, re_path

from .views import icons, groups


app_name = 'wagtailicons'
urlpatterns = [
    path('', icons.index.as_view(), name='index'),
    path('add/', icons.add.as_view(), name='add'),
    path('edit/', icons.edit.as_view(), name='edit'),
    # groups urls
    path('groups/', groups.index.as_view(), name='groups'),
    path('groups/add/', groups.add.as_view(), name='add_group'),
]
