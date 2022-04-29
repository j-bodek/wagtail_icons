
from wagtail_icons.models import Icon
from wagtail_icons.forms import GroupForm
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from wagtail.admin import messages
from wagtail_icons.models import Group, Icon


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

            icons = request.POST.getlist("icons")
            return_data = {}
            form = GroupForm(request.POST)

            if form.is_valid():
                # Save it
                group = form.save(commit=False)
                group.save()
                if icons:
                    icons = Icon.objects.filter(id__in=icons)
                    group.icons.add(*icons)
                    group.save()
                    messages.success(request, f"Successfully created {group.title}! With {icons.count()} icon{'s' if icons.count()>1 else ''}.")
                else:
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
            'icons':Icon.objects.all(),
        })
        return context

