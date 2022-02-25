from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.contrib.staticfiles.utils import get_files

ALLOWED_EXTENSIONS = ['svg', 'png']

class IconsField(models.CharField):
    # s = StaticFilesStorage()
    # ICONS = list(set([x.split(".", 1)[0] for x in list(get_files(s, location="icons/icon"))]))
    # ICONS = ((x+'.svg',x.replace("eve/icons\\","")) for x in sorted(ICONS))
    ICONS = ()

    def __init__(self, *args, **kwargs):

        kwargs.setdefault('max_length', 70)
        kwargs.setdefault('null', True)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('choices', self.ICONS)
        super().__init__(*args, **kwargs)