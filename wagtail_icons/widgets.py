from wagtail_icons.models.upload import Icon
from wagtail import VERSION as WAGTAIL_VERSION
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from generic_chooser.widgets import AdminChooser
from django.core.exceptions import ObjectDoesNotExist


class AdminIconChooser(AdminChooser):
    choose_one_text = _("Choose an SVG")
    choose_another_text = _("Choose another SVG")
    link_to_chosen_text = _("Edit this SVG")
    model = Icon
    choose_modal_url_name = 'wagtail_icons:choose'
    clear_choice_text = _("Clear choice")
    template = 'wagtailsvg/widgets/chooser.html'

    def get_value_data(self, value):
        if value is None:
            icon = None
        elif isinstance(value, self.model):
            icon = value
        else:
            icon = self.model.objects.get(pk=value)


        return {
            'value': None if not icon else icon.pk,
            'title': '' if not icon else icon.title,
            # 'edit_item_url': None if not icon else self.get_edit_item_url(icon),
            'preview_url': None if not icon else icon.file.url,
        }

    def render_html(self, name, value, attrs):
        if WAGTAIL_VERSION >= (2, 12):
            value_data = value
        else:
            value_data = self.get_value_data(value)

        original_field_html = self.render_input_html(name, value_data['value'], attrs)
        return render_to_string(self.template, {
            'widget': self,
            'original_field_html': original_field_html,
            'attrs': attrs,
            'is_empty': value_data['value'] is None,
            'title': value_data['title'],
            'choose_modal_url': self.get_choose_modal_url(),
            'preview_url': value_data['preview_url']
        })

    class Media:
        js = [
            'generic_chooser/js/chooser-modal.js',
            'wagtail_icons/js/icon_chooser_modal.js',
        ]
