from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.contrib.staticfiles.utils import get_files
from icons.models.upload import Icon



class IconsField(models.CharField):
    ICONS = Icon.objects.all().values_list('file', 'title')

    def __init__(self, *args, **kwargs):

        kwargs.setdefault('max_length', 70)
        kwargs.setdefault('null', True)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('choices', self.ICONS)
        super().__init__(*args, **kwargs)