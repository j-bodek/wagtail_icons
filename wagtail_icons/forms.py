from django.forms import ModelForm
from .models import Icon, Group
from django import forms

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
            'slug': forms.TextInput(attrs={'placeholder':'Slug should contain only lowercase letters, numbers and -,_'})
        }