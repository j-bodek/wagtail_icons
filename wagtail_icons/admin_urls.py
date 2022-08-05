from django.urls import path

from wagtail_icons.views import icons, groups


app_name = 'wagtailicons'
urlpatterns = [
    path('', icons.IconsIndexView.as_view(), name='index'),
    path('add/', icons.IconsAddView.as_view(), name='add'),
    path('edit/', icons.IconsEditView.as_view(), name='edit'),
    # groups urls
    path('groups/', groups.GroupIndexView.as_view(), name='groups'),
    path('groups/add/', groups.GroupAddView.as_view(), name='add_group'),
]
