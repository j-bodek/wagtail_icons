from django.forms.widgets import ChoiceWidget
from django.forms import Media
from django.template import loader
from django.utils.safestring import mark_safe
from icons.models.upload import Icon


class IconsChooserWidget(ChoiceWidget):

    class Media:
        css = {
            "all": (
                'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.4.0/font/bootstrap-icons.css',
                "icons/style/iconchooser.css",
            )
        }
        js = [
            "icons/js/iconchooser.js"
        ]


    input_type = 'radio'
    template_name = 'icons/widgets/icons_widget.html'
    option_template_name = 'icons/widgets/icons_option_widget.html'

