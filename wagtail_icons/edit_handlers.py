from .widgets import IconsChooserWidget
from wagtail.admin.edit_handlers import FieldPanel

class IconsChooserPanel(FieldPanel):
    def __init__(self, field_name, group_name, *args, **kwargs):
        super().__init__(field_name, *args, **kwargs)
        self.group_name = group_name

    def clone_kwargs(self):
        kwargs = super().clone_kwargs()
        kwargs.update(
            group_name=self.group_name,
        )
        return kwargs
    def widget_overrides(self):
        return {
            self.field_name: IconsChooserWidget(),
        }
