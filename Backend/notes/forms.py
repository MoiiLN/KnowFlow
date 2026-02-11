from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms

from .models import Note


class AddNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'content')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {'novalidate': True}
        self.helper.layout = Layout(
            FloatingField('title'),
            FloatingField('content'),
            Submit('create', 'Create', css_class='w-100 mt-2 mb-2'),
        )


class EditNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'content')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {'novalidate': True}
        self.helper.layout = Layout(
            FloatingField('title'),
            FloatingField('content'),
            Submit('edit', 'Edit', css_class='w-100 mt-2 mb-2'),
        )
