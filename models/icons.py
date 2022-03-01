from django.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel
from ..fields import IconsField
from ..edit_handlers import IconsChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image
from icons.models.upload import Icon

# Create your models here.


class iconsPage(Page):
    template_name = 'icons/icons.html'
    icon = IconsField()

    cover = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        IconsChooserPanel('icon'),
        ImageChooserPanel('cover'),
    ]