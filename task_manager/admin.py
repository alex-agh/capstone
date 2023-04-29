from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import CodingTask

class CodingTaskForm(ModelForm):
    class Meta:
        model = CodingTask
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        markdown_file = cleaned_data.get('markdown_file')
        test_file = cleaned_data.get('test_file')
        initial_file = cleaned_data.get('initial_file')
        if markdown_file and test_file:
            if not markdown_file.name.endswith('.md'):
                raise ValidationError("Markdown file must have a .md extension")
            if not test_file.name.endswith('.cs'):
                raise ValidationError("Test file must have a .cs extension")
            if not initial_file.name.endswith('.cs'):
                raise ValidationError("Initial CS file must have a .cs extension")

class CodingTaskAdmin(admin.ModelAdmin):
    form = CodingTaskForm

admin.site.register(CodingTask, CodingTaskAdmin)