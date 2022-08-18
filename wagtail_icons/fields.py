from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail_icons.models.upload import Icon


class IconsField(models.ForeignKey):

    def __init__(self, group=None, *args, **kwargs):
        kwargs.setdefault('to', Icon)
        kwargs.setdefault('on_delete', models.SET_NULL)
        kwargs.setdefault('null', True)
        kwargs.setdefault('blank', True)
        super().__init__(*args, **kwargs)

