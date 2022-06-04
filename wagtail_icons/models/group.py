import os
from django.db import models
from wagtail.core.utils import string_to_ascii
from wagtail.images.models import get_upload_to
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
from wagtail_icons.models import Icon

ALLOWED_EXTENSIONS = ['svg']

class Group(models.Model): 
    title = models.CharField(max_length=255, verbose_name=_('title'), unique=True, blank=False, null=False)
    slug = models.CharField(max_length=255, blank=False, null=False, unique=True)
    icons = models.ManyToManyField(Icon, blank=True)
    edited = models.DateTimeField('edited', auto_now=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True, blank=False, null=False, editable=False, db_index=True)