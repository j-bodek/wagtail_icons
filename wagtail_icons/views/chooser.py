from wagtail_icons.models.upload import Icon
from django.utils.translation import gettext as _
from generic_chooser.views import (
    ModelChooserViewSet,
    ChooserListingTabMixin,
    ModelChooserMixin
)

# Widget icons listing and choose view

class IconsChooserListingTab(ChooserListingTabMixin):
    results_template = 'wagtail_icons/widgets/chooser_results.html'

    def get_row_data(self, item):
        return {
            'choose_url': self.get_chosen_url(item),
            'title': item.title,
            'url': item.file.url,
        }

class IconsModelChooserMixin(ModelChooserMixin):
    def get_chosen_response_data(self, item):
        response_data = super().get_chosen_response_data(item)
        response_data['preview_url'] = item.file.url
        return response_data

    def get_object_list(self, search_term=None, **kwargs):
        if search_term:
            return Icon.objects.filter(title__icontains=search_term)
        return self.get_unfiltered_object_list()


class IconsChooserViewSet(ModelChooserViewSet):
    model = Icon
    icon = 'image'
    page_title = _("Choose an Icon")
    listing_tab_mixin_class = IconsChooserListingTab
    chooser_mixin_class = IconsModelChooserMixin
    per_page = 20