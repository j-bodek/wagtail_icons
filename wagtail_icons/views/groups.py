
from wagtail_icons.models import Icon
from wagtail_icons.forms import GroupForm
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from wagtail.admin import messages
from wagtail_icons.models import Group


class index(TemplateView):
    template_name = 'wagtail_icons/groups/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'groups': Group.objects.all(),
        })

        return context

class add(TemplateView):
    template_name = 'wagtail_icons/groups/add.html'

    def post(self, request):
        if request.method == 'POST':

            return_data = {}
            form = GroupForm(request.POST)

            if form.is_valid():
                # Save it
                group = form.save(commit=False)
                group.save()
                form.save_m2m()
                # return_data = {"icon_id":group.id, 'group_slug':group.slug, 'group_title':group.title, "message":"Success"}
                messages.success(request, f"Successfully created {group.title}!")
                return redirect('wagtailicons:groups')
            else:
                error = '\n'.join([f"{key} - {value[0].get('message')}" for key, value in form.errors.get_json_data().items()])
                messages.error(request, error)
                return render(request, self.template_name, context=self.get_context_data())



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = GroupForm()

        context.update({
            'form': form,
        })
        return context

