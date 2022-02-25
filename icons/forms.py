from django.forms import ModelForm
from .models import Icon

class IconForm(ModelForm):
    class Meta:
        model = Icon
        fields = '__all__'