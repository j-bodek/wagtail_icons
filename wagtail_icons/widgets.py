from django.forms.widgets import ChoiceWidget
from django.forms import Media
from django.template import loader
from django.utils.safestring import mark_safe
from wagtail_icons.models.upload import Icon


class IconsChooserWidget(ChoiceWidget):

    class Media:
        css = {
            "all": (
                'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.4.0/font/bootstrap-icons.css',
                "wagtail_icons/style/iconchooser.css",
            )
        }
        js = [
            "wagtail_icons/js/iconchooser.js"
        ]


    input_type = 'radio'
    template_name = 'wagtail_icons/widgets/icons_widget.html'
    option_template_name = 'wagtail_icons/widgets/icons_option_widget.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        optgroups = self.optgroups(name, context['widget']['value'], attrs)
        if not True in list(set([choice[1][0]['selected'] for choice in optgroups])): optgroups[0][1][0]['selected'] = True
        context['widget']['optgroups'] = optgroups
        return context
