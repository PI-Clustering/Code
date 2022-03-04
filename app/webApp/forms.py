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
ALGO_CHOICES2 = [('incremental', 'incremental'), ('median', 'median'), ('exact', 'exact')]

class ParametersForm(forms.Form):

    dataset = forms.ChoiceField(
        required=True,
        choices=DATASET_CHOICES,
        label="Which dataset are you using?"
    )
    use_precomputed = forms.BooleanField(
        required=False,
        label="Use precomputed?"
    )
    limit_to = forms.IntegerField(
        required=False,
        initial=80,
        min_value=1,
        max_value=100,
        label="How many percent of nodes to limit to?"
    )
    nb_subcluster = forms.IntegerField(
        required=True,
        initial=2,
        min_value=2,
        label="How many subcluster"
    )
    query_edge = forms.BooleanField(
        required=False,
        label="Query edge?"
    )
    evaluate = forms.BooleanField(
        required=False,
        label="Evaluate the cluster ?"
    )


class NodesForm(forms.Form):

    method = forms.ChoiceField(
        required=True,
        choices=ALGO_CHOICES2,
        label="Which dataset are you using?"
    )
    how_many = forms.IntegerField(
        required=True,
        initial=1,
        min_value=1,
        label="How many nodes to add?"
    )
    use_real_data = forms.BooleanField(
        required=False,
        label="Use Real Data?"
    )
    evaluate = forms.BooleanField(
        required=False,
        label="Evaluate the cluster ?"
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
