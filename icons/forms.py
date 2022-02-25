from django.forms import ModelForm
from .models import Icon
from django import forms

class IconForm(ModelForm):
    class Meta:
        model = Icon
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'If not specified title will be file name'})
        }