from django.utils.html import format_html
from django.utils.functional import cached_property

try:
    from wagtail.blocks import ChooserBlock
except ImportError:
    from wagtail.core.blocks import ChooserBlock

from wagtail.images.shortcuts import get_rendition_or_not_found


class IconsChooserBlock(ChooserBlock):

    @cached_property
    def target_model(self):
        from wagtail_icons.models import Icon
        return Icon

    @cached_property
    def widget(self):
        from wagtail_icons.widgets import AdminIconChooser
        return AdminIconChooser()

    def get_form_state(self, value):
        return self.widget.get_value_data(value)
