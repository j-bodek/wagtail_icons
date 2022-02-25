from django.shortcuts import render

from wagtail.admin.views.generic.multiple_upload import AddView as BaseAddView
from wagtail.images import get_image_model
from icons.fields import ALLOWED_EXTENSIONS
from wagtail.images.forms import get_image_form, get_image_multi_form
from wagtail.images.models import UploadedImage
from wagtail.images.permissions import permission_policy

from wagtail.documents import get_document_model
from wagtail.documents.forms import get_document_form, get_document_multi_form
from wagtail.documents.models import UploadedDocument
# from wagtail.documents.permissions import permission_policy
from wagtail.documents.models import UploadedDocument
from icons.models import Icon
from icons.forms import IconForm
from django.views.generic.base import TemplateView
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse


def index(request):

    return render(request, 'icons/icons_page/index.html')




class add(TemplateView):
    template_name = 'icons/icons_page/add.html'

    def post(self, request):
        if not request.FILES:
            return HttpResponseBadRequest("Please upload a file")
        

        form = IconForm(request.POST, request.FILES)
        print(request.POST)
        print(request.FILES)

        if form.is_valid():
            # Save it
            icon = form.save(commit=False)
            icon.uploaded_by_user = self.request.user
            icon.file_size = icon.file.size
            icon.file.seek(0)

            icon.save()
            return HttpResponse("Icon successfully uploaded")
        

        return HttpResponse("Error")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = IconForm()

        context.update({
            'form': form,
        })

        return context
