# Wagtail Icons

## Install

```
pip install -i https://test.pypi.org/simple/ wagtail-icons==0.0.4
```

Then add `wagtailextraicons` to your installed apps:

```
INSTALLED_APPS = [
    ...
    'wagtail_icons'
]
```

## Usage


```python
from wagtail_icons.edit_handlers import IconsChooserPanel
from wagtail_icons.models.upload import Icon

class iconsPage(Page):
    template_name = 'yourapp/yourtemplate'
    icon = IconsField()

    content_panels = Page.content_panels + [
        IconsChooserPanel('icon'),
    ]
```
