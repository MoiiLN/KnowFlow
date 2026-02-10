from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms

from .models import Knowtionary


class AddKnowtionaryForm(forms.ModelForm):
    class Meta:
        model = Knowtionary
        fields = ('name', 'description', 'question', 'answer', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {'novalidate': True}
        self.helper.layout = Layout(
            FloatingField('name'),
            FloatingField('description'),
            FloatingField('question'),
            FloatingField('answer'),
            FloatingField('image'),
            Submit('create', 'Create', css_class='w-100 mt-2 mb-2'),
        )


class EditKnowtionaryForm(forms.ModelForm):
    class Meta:
        model = Knowtionary
        fields = ('name', 'description', 'question', 'answer', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {'novalidate': True}
        self.helper.layout = Layout(
            FloatingField('name'),
            FloatingField('description'),
            FloatingField('question'),
            FloatingField('answer'),
            FloatingField('image'),
            Submit('edit', 'Edit', css_class='w-100 mt-2 mb-2'),
        )
