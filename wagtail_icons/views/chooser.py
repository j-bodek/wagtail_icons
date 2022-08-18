from tokenize import group
from wagtail_icons.models.upload import Icon
from wagtail_icons.models.group import Group
from django.utils.translation import gettext as _
from generic_chooser.views import (
    ModelChooserViewSet,
    ChooserListingTabMixin,
    ModelChooserMixin
)

# Widget icons listing and choose view

class IconsChooserListingTab(ChooserListingTabMixin):
    results_template = 'wagtail_icons/widgets/chooser_results.html'
    listing_tab_template = 'wagtail_icons/widgets/_listing_tab.html'

    def get_row_data(self, item):
        return {
            'choose_url': self.get_chosen_url(item),
            'title': item.title,
            'url': item.file.url,
        }

    def get_listing_tab_context_data(self):
        # parameters passed to get_object_list / get_paginated_object_list to modify results
        context = super().get_listing_tab_context_data()

        group_slug = self.request.GET.get('gs')
        if group_slug and not Group.objects.filter(slug=group_slug).exists():
            context.update({
                'is_searchable': False,
                'invalid_group': True,
                'group_slug':group_slug,
            })

        return context


class IconsModelChooserMixin(ModelChooserMixin):
    preserve_url_parameters = ['gs',]

    def get_chosen_response_data(self, item):
        response_data = super().get_chosen_response_data(item)
        response_data['preview_url'] = item.file.url
        return response_data

    def get_unfiltered_object_list(self):
        objects = super().get_unfiltered_object_list()
        group_slug = self.request.GET.get('gs')
        if not group_slug:
            return objects
        
        try:
            group = Group.objects.get(slug=group_slug)
            objects = group.icons.all()
        except Group.DoesNotExist:
            objects = Icon.objects.none()
        return objects

    def get_object_list(self, search_term=None, **kwargs):
        if search_term:
            return self.get_unfiltered_object_list().filter(title__icontains=search_term)
        return self.get_unfiltered_object_list()


class IconsChooserViewSet(ModelChooserViewSet):
    model = Icon
    icon = 'image'
    page_title = _("Choose an Icon")
    listing_tab_mixin_class = IconsChooserListingTab
    chooser_mixin_class = IconsModelChooserMixin
    per_page = 20