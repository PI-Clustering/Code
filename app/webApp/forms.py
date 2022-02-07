from shelve import DbfilenameShelf
from django import forms
# from .models import Document
from .models import Document


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


DATASET_CHOICES = [
    ('ldbc', 'LDBC'),
    ('covid-19', 'Covid 19'),
]
ALGO_CHOICES = [('param1', 'display name 1'), ('param2', 'display name 2')]


class ParametersForm(forms.Form):
    algo = forms.ChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=ALGO_CHOICES,
    )

# class DocumentForm(forms.ModelForm):
#     class Meta:
#         model = Document
#         fields = ('description', 'document', )


class DocumentForm(forms.ModelForm):
    # global Settings_Apify
    class Meta:
        model = Document
        # widgets = {'Attributes': forms.Textarea(), }
        fields = ('description', 'document',)

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Name:'})
        self.fields['document'].widget.attrs.update(
            {'class': 'form-file', 'type': 'file', 'id': 'formFile'})
