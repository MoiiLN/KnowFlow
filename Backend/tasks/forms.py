from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms

from .models import TaskFlow


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = TaskFlow
        fields = ('name', 'description', 'finished_at')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {'novalidate': True}
        self.helper.layout = Layout(
            FloatingField('name'),
            FloatingField('description'),
            FloatingField('finished_at'),
            Submit('create', 'Create', css_class='w-100 mt-2 mb-2'),
        )


class EditTaskForm(forms.ModelForm):
    class Meta:
        model = TaskFlow
        fields = ('name', 'description', 'finished_at')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {'novalidate': True}
        self.helper.layout = Layout(
            FloatingField('name'),
            FloatingField('description'),
            FloatingField('finished_at'),
            Submit('edit', 'Edit', css_class='w-100 mt-2 mb-2'),
        )
