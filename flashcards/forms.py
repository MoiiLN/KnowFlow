from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms

from .models import FlowCard


class AddFlowCardForm(forms.ModelForm):
    class Meta:
        model = FlowCard
        fields = ('name', 'term', 'definition')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {'novalidate': True}
        self.helper.layout = Layout(
            FloatingField('name'),
            FloatingField('term'),
            FloatingField('definition'),
            Submit('create', 'Create', css_class='w-100 mt-2 mb-2'),
        )


class EditFlowCardForm(forms.ModelForm):
    class Meta:
        model = FlowCard
        fields = ('name', 'term', 'definition')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {'novalidate': True}
        self.helper.layout = Layout(
            FloatingField('name'),
            FloatingField('term'),
            FloatingField('definition'),
            Submit('edit', 'Edit', css_class='w-100 mt-2 mb-2'),
        )
