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
from wagtail_icons.models import Icon, Group
from wagtail_icons.forms import IconForm
from wagtail.admin import messages
from django.views.generic.base import TemplateView
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
import json
# from icons.fields import IconsField


class index(TemplateView):
    template_name = 'wagtail_icons/icons_page/index.html'


    def post(self, request):
        if request.POST.getlist("icons"):
            if 'type' in request.POST.dict().keys() and request.POST.get("type") == 'delete':
                icons_ids = request.POST.getlist("icons")
                group_id = request.POST.get('group','')
                # if group_id is not specified
                if not group_id and icons_ids:
                    Icon.objects.filter(id__in=icons_ids).delete()
                elif group_id and icons_ids:
                    try:
                        group = Group.objects.get(id=group_id)
                        icons = Icon.objects.filter(id__in=icons_ids)
                        group.icons.remove(*icons)
                    except:
                        group = None

                context = self.get_context_data()
                # update context if group_id
                if group_id:
                    if group:
                        icons = group.icons.all()
                    else:
                        icons = None
                    context.update({
                        'icons':icons,
                        'group':group,
                    })                
            
                return render(request, self.template_name, context=context)

        return JsonResponse({"message":"No icons specified"})

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.GET.get('group',''):
            group_id = request.GET.get('group','')
            try:
                group = Group.objects.get(id=group_id)
                icons = group.icons.all()
            except:
                group, icons = None, None
            context.update({
                'icons':icons,
                'group':group,
            })
        return self.render_to_response(context)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        icons = Icon.objects.all()

        context.update({
            'icons': icons,
        })

        return context


class add(TemplateView):
    template_name = 'wagtail_icons/icons_page/add.html'

    def post(self, request, *args, **kwargs):
        group_id = request.POST.get('group','')
        custom_action = request.POST.get('type')
        # update conetxt
        context = self.get_context_data(**kwargs)
        if group_id:
            try:
                # display icons that are not in group
                group = Group.objects.get(id=group_id)
                icons = group.icons.all()
                icons = Icon.objects.all().exclude(id__in=list(icons.values_list('id', flat=True)))
            except:
                group, icons = None, None
            context.update({
                'icons':icons,
                'group':group,
            })


        if request.POST.get('action') == 'upload':

            if not request.FILES:
                return HttpResponseBadRequest("Please upload a file")
            
            # get specified title or file title if specified doesn't exist

            return_data = []
            icons = request.FILES.getlist('icons')
            urls = request.POST.getlist('urls')
            # get group if group_id
            if group_id:
                try:
                    group = Group.objects.get(id=group_id)
                except:
                    group = None
            else:
                group = None

            for file, url in zip(icons, urls):

                file_title = request.POST.get('title') if request.POST.get('title') and len(icons) == 1 else file.name.rsplit(".", 1)[0]

                form = IconForm({
                    'title': file_title,
                },{
                    'file': file,
                })

                if form.is_valid():
                    # Save it
                    icon = form.save(commit=False)
                    icon.uploaded_by_user = self.request.user
                    icon.file_size = icon.file.size
                    icon.file.seek(0)
                    icon.save()
                    # add icon to group if specified
                    if group:
                        group.icons.add(icon)
                        group.save()
                    return_data.append({"icon_id":icon.id, "icon_url":url, 'icon_title':file.name, "message":"Success"})
                else:
                    if 'file' in form.errors.get_json_data().keys() and form.errors.get_json_data()['file']:
                        error = form.errors.get_json_data()['file'][0]
                        return_data.append(error)

            return JsonResponse(return_data, safe=False)


            

        elif request.POST.get('action') == 'update' and not group_id:
            if Icon.objects.filter(id=request.POST.get('icon_id')):
                update_icon = Icon.objects.filter(id=request.POST.get('icon_id'))
                update_icon.update(title=request.POST.get('title'))
                return JsonResponse({"message":"Icon Updated"})

            return JsonResponse({"message":"Error"})

        elif request.POST.get('action') == 'delete':
            if Icon.objects.filter(id=request.POST.get('icon_id')):
                delete_icon = get_object_or_404(Icon, id=request.POST.get('icon_id'))
                delete_icon.delete()
                return JsonResponse({"message":"Icon Deleted"})

            return JsonResponse({"message":"Error"})
        elif custom_action == 'add_existing' and group_id:
            icons = request.POST.getlist("icons")
            icons = Icon.objects.filter(id__in=icons)
        
            try:
                group = Group.objects.get(id=group_id)
                group.icons.add(*icons)
                group.save()
                # update context
                context.update({
                'icons':Icon.objects.all().exclude(id__in=list(icons.values_list('id', flat=True))),
                'group':group,
                })
                messages.success(request, f"Successfully added {icons.count()} icon{'s' if icons.count()>1 else ''} to group : {group.title}")
                return render(request, self.template_name, context=context)
            except Exception as e:
                messages.error(request, e)
                return render(request, self.template_name, context=context)
        else:
            return JsonResponse({"message":"Invalid action"})


    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.GET.get('group',''):
            group_id = request.GET.get('group','')
            try:
                # display icons that are not in group
                group = Group.objects.get(id=group_id)
                icons = group.icons.all()
                icons = Icon.objects.all().exclude(id__in=list(icons.values_list('id', flat=True)))
            except:
                group, icons = None, None
            context.update({
                'icons':icons,
                'group':group,
            })
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = IconForm()

        context.update({
            'form': form,
        })

        return context


class edit(TemplateView):
    template_name = 'wagtail_icons/icons_page/edit.html'

    def post(self, request, *args, **kwargs):
        if request.POST.getlist("icons"):
            if 'type' in request.POST.dict().keys() and request.POST.get('type') == 'edit':
                
                context = self.get_context_data(**kwargs)
                icons_ids = request.POST.getlist("icons")
                context.update({
                    'icons': Icon.objects.filter(id__in=icons_ids),
                })
                return render(request, self.template_name, context=context)

        if 'type' in request.POST.dict().keys() and request.POST.get('type') == 'update':
            if Icon.objects.filter(id=request.POST.get('icon_id')):
                update_icon = Icon.objects.filter(id=request.POST.get('icon_id'))
                update_icon.update(title=request.POST.get('title'))
                return JsonResponse({"message":"Icon Updated"})

            return JsonResponse({"message":"Error"})

        if 'type' in request.POST.dict().keys() and request.POST.get('type') == 'delete':
            if Icon.objects.filter(id=request.POST.get('icon_id')):
                delete_icon = get_object_or_404(Icon, id=request.POST.get('icon_id'))
                delete_icon.delete()
                return JsonResponse({"message":"Icon Deleted"})

            return JsonResponse({"message":"Error"})


        return JsonResponse({"message":"No Icons Choosed"})

