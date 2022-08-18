from django.utils.functional import cached_property

try:
    from wagtail.blocks import ChooserBlock
except ImportError:
    from wagtail.core.blocks import ChooserBlock

class IconsChooserBlock(ChooserBlock):
    def __init__(self, group=None, **kwargs):
        super().__init__(**kwargs)
        self.group = group

    @cached_property
    def target_model(self):
        from wagtail_icons.models import Icon
        return Icon

    @cached_property
    def widget(self):
        from wagtail_icons.widgets import AdminIconChooser
        return AdminIconChooser(group=self.group)

    def get_form_state(self, value):
        return self.widget.get_value_data(value)
