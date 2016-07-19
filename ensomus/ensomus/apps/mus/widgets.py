"""
Custom widgets for NXT LVL
"""
from django import forms
from django.utils.safestring import mark_safe


class PlainTextWidget(forms.TextInput):
    """
    Allows field to displayed as text (and hidden to have the value available for validation)
    """
    input_type = 'hidden'

    def __init__(self, model=None, *args, **kwargs):
        super(PlainTextWidget, self).__init__(*args, **kwargs)
        self.attrs = kwargs.get('attrs', {})
        self.model = model

    def render(self, name, value, *args, **kwargs):
        if self.model:
            text = unicode(self.model.objects.get(pk=value)) if value is not None and value != '' else '-'
        else:
            text = value
        html = '%s %s' % (super(PlainTextWidget, self).render(name, value, self.attrs), text)
        return mark_safe(html)