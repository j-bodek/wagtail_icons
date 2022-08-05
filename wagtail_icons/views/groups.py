
from wagtail_icons.models import Icon
from wagtail_icons.forms import GroupForm
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from wagtail.admin import messages
from wagtail_icons.models import Group, Icon
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from wagtail.admin.forms.search import SearchForm
from django.utils.translation import gettext as _
from django.db.models import Q
from django.db.models import Count


class GroupIndexView(TemplateView):
    template_name = 'wagtail_icons/groups/index.html'

    def post(self, request):
        if request.POST.get("type") == 'delete':
            try:
                group_ids = request.POST.getlist("groups")
                groups = Group.objects.filter(id__in=group_ids)
                groups_num = groups.count()
                groups.delete()
                messages.success(request, f"Successfully deleted {groups_num} group{'s' if groups_num > 1 else ''}!")
                return render(request, self.template_name, context=self.get_context_data())
            except Exception as e:
                messages.error(request, e)
                return render(request, self.template_name, context=self.get_context_data())


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups  = Group.objects.all()

        # Search
        query_string = None
        if 'q' in self.request.GET:
            self.search_form = SearchForm(self.request.GET, placeholder=_("Search groups"))
            if self.search_form.is_valid():
                query_string = self.search_form.cleaned_data['q']
                groups = groups.filter(Q(title__icontains=query_string.lower()) | Q(slug__icontains=query_string.lower()))
        else:
            self.search_form = SearchForm(placeholder=_("Search groups"))

        # ordering
        if self.request.GET.get("ordering") :
            if not self.request.GET.get("ordering").endswith('icons_num'):
                ordering = self.request.GET.get("ordering")
                groups = groups.order_by(ordering)
            else:
                ordering = self.request.GET.get("ordering")
                groups = groups.annotate(icons_num=Count('icons')).order_by(ordering)
        else:
            ordering = '-edited'
            groups = groups.order_by(ordering)

        # Pagination
        paginator = Paginator(groups, 15)
        page_num = self.request.GET.get("p")
        try:
            groups = paginator.page(page_num)
        except PageNotAnInteger:
            groups = paginator.page(1)
        except EmptyPage:
            groups = paginator.page(paginator.num_pages)

        context.update({
                'groups':groups,
                'search_form':self.search_form,
                'query_string':query_string,
                'ordering': ordering,
        })

        return context


class GroupAddView(TemplateView):
    template_name = 'wagtail_icons/groups/add.html'

    def post(self, request):
        if request.method == 'POST':

            icons = request.POST.getlist("icons")
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
            'icons':Icon.objects.all().order_by('-created_at'),
        })
        return context

