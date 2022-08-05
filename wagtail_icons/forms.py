from django.forms import ModelForm
from .models import Icon, Group
from django import forms
import re

class IconForm(ModelForm):
    class Meta:
        model = Icon
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'If not specified title will be file name', 'id':'titleinput', 'max_length':255}),
            'file': forms.FileInput(attrs={'id':'fileinput', 'multiple':'multiple'}),
        }


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'Group Title'}),
            'slug': forms.TextInput(attrs={'placeholder':'Slug field can contains only lowercase letters, numbers, underscore "_" and dashes "-"'})
        }

    def clean(self):
        super(GroupForm, self).clean()
        slug = self.cleaned_data.get("slug")
        # validate slug field
        if not re.match(r'^[a-z0-9_-]+$', slug):
            self._errors['slug'] = self.error_class([
                'Slug field can contains only lowercase letters, numbers, underscore "_" and dashes "-"'])

        # return any errors if found
        return self.cleaned_data