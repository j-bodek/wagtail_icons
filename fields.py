from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.contrib.staticfiles.utils import get_files
from icons.models.upload import Icon


class IconsField(models.ForeignKey):
    # ICONS = Icon.objects.all().values_list('file', 'title')
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('to', 'Icon')
        kwargs.setdefault('on_delete', models.SET_NULL)
        kwargs.setdefault('null', True)
        kwargs.setdefault('blank', True)
        super().__init__(*args, **kwargs)