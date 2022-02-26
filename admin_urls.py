from django.urls import path

from .views import icons


app_name = 'wagtailicons'
urlpatterns = [
    path('', icons.index.as_view(), name='index'),
    path('add/', icons.add.as_view(), name='add'),
]
