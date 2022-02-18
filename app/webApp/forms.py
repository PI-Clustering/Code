from django import forms
from .models import Document


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


DATASET_CHOICES = [
    ('ldbc', 'LDBC'),
    ('covid-19', 'Covid 19'),
    ('fib25', 'FIB 25')
]
ALGO_CHOICES = [('k-mean', 'K-Means'), ('algo2', 'Dummy 2')]


class ParametersForm(forms.Form):

    dataset = forms.ChoiceField(
        required=True,
        choices=DATASET_CHOICES,
        label="Which dataset are you using?"
    )
    method = forms.ChoiceField(
        required=True,
        choices=ALGO_CHOICES,
        label="Which method do you want?"
    )
    has_limit = forms.BooleanField(
        required=False,
        label="Limit data?"
    )
    limit_to = forms.IntegerField(
        required=False,
        initial=100,
        min_value=1,
        max_value=100,
        label="How many percent of nodes to limit to?"
    )
    use_incremental = forms.BooleanField(
        required=False,
        label="Use Incremental Approach"
    )
    nb_subcluster = forms.IntegerField(
        required=True,
        initial=2,
        min_value=2,
        label="How many subcluster"
    )


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
