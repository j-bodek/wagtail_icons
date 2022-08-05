from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail_icons.models.upload import Icon
from django.forms.models import ModelChoiceField
from wagtail_icons.models import Group


class IconsField(models.ForeignKey):
    group_model = Group

    def __init__(self, group=None, *args, **kwargs):
        kwargs.setdefault('to', Icon)
        kwargs.setdefault('on_delete', models.SET_NULL)
        kwargs.setdefault('null', True)
        kwargs.setdefault('blank', True)
        super().__init__(*args, **kwargs)
        self.group = group
    
    def formfield(self, *, using=None, **kwargs):
        if isinstance(self.remote_field.model, str):
            raise ValueError("Cannot create form field for %r yet, because "
                             "its related model %r has not been loaded yet" %
                             (self.name, self.remote_field.model))
        return super().formfield(**{
            'form_class': ModelChoiceField,
            'queryset': self.get_queryset(using=using),
            'to_field_name': self.remote_field.field_name,
            **kwargs,
            'blank': self.blank,
        })

    def get_queryset(self, using):
        if self.group == None:
            return self.remote_field.model._default_manager.using(using)
        try:
            group = self.group_model.objects.get(slug=self.group)
        except Group.DoesNotExist:
            group = self.group_model.objects.get(title=self.group)
        return group.icons.using(using)

