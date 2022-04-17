from django.shortcuts import render, redirect

from wagtail.admin.views.generic.multiple_upload import AddView as BaseAddView
from wagtail.images import get_image_model
from wagtail.images.forms import get_image_form, get_image_multi_form
from wagtail.images.models import UploadedImage
from wagtail.images.permissions import permission_policy

from wagtail.documents import get_document_model
from wagtail.documents.forms import get_document_form, get_document_multi_form
from wagtail.documents.models import UploadedDocument
# from wagtail.documents.permissions import permission_policy
from wagtail.documents.models import UploadedDocument
from wagtail_icons.models import Icon
from wagtail_icons.forms import IconForm
from django.views.generic.base import TemplateView
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
import json
# from icons.fields import IconsField


class index(TemplateView):
    template_name = 'wagtail_icons/groups/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

