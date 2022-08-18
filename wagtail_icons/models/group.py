from django.db import models
try:
    from wagtail.utils import string_to_ascii
except ImportError:
    from wagtail.core.utils import string_to_ascii
from django.utils.translation import gettext_lazy as _
from wagtail_icons.models import Icon

ALLOWED_EXTENSIONS = ['svg']

class Group(models.Model): 
    title = models.CharField(max_length=255, verbose_name=_('title'), unique=True, blank=False, null=False)
    slug = models.CharField(max_length=255, blank=False, null=False, unique=True)
    icons = models.ManyToManyField(Icon, blank=True)
    edited = models.DateTimeField('edited', auto_now=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True, blank=False, null=False, editable=False, db_index=True)