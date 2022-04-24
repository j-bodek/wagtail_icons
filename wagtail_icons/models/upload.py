import os
from django.db import models
from wagtail.core.utils import string_to_ascii
from wagtail.images.models import get_upload_to
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator

ALLOWED_EXTENSIONS = ['svg']

class Icon(models.Model): 
    title = models.CharField(max_length=255, verbose_name=_('title'), blank=True)
    file = models.FileField(
        verbose_name=_('file'), 
        upload_to=get_upload_to,
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)],
    )
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True, db_index=True)
    uploaded_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('uploaded by user'),
        null=True, blank=True, editable=False, on_delete=models.SET_NULL
    )


    file_size = models.PositiveIntegerField(null=True, editable=False)

    # create full path where file should be uploaded
    def get_upload_to(self, filename):
        folder_name = 'icons'
        filename = self.file.field.storage.get_valid_name(filename)

        # do a unidecode in the filename and then
        # replace non-ascii characters in filename with _ , to sidestep issues with filesystem encoding
        filename = "".join((i if ord(i) < 128 else '_') for i in string_to_ascii(filename))

        # Truncate filename so it fits in the 100 character limit
        # https://code.djangoproject.com/ticket/9893
        full_path = os.path.join(folder_name, filename)
        if len(full_path) >= 95:
            chars_to_trim = len(full_path) - 94
            prefix, extension = os.path.splitext(filename)
            filename = prefix[:-chars_to_trim] + extension
            full_path = os.path.join(folder_name, filename)

        return full_path

    def __str__(self):
        return self.title


# These two auto-delete files from filesystem

@receiver(models.signals.post_delete, sender=Icon)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Icon` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

@receiver(models.signals.pre_save, sender=Icon)
def auto_delete_file_on_change(sender, instance, **kwargs):
    
    """
    Deletes old file from filesystem
    when corresponding `Icon` object is updated
    with new file.
    """
    if not instance.pk:
        return False
