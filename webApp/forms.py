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
ALGO_CHOICES2 = [('I-GMM-D', 'I-GMM-D'), ('GMM-D', 'GMM-D')]

class ParametersForm(forms.Form):

    dataset = forms.ChoiceField(
        required=True,
        choices=DATASET_CHOICES,
        label="Which dataset are you using?"
    )
    limit_to = forms.IntegerField(
        required=False,
        initial=80,
        min_value=1,
        max_value=100,
        label="Percentage of node to consider?"
    )
    nb_subcluster = forms.IntegerField(
        required=True,
        initial=2,
        min_value=2,
        label="Subclusters to be discovered at each iteration"
    )
    query_edge = forms.BooleanField(
        required=False,
        initial=True,
        label="Include original edge labels"
    )
    evaluate = forms.BooleanField(
        required=False,
        label="Keep track of this cluster evaluation?"
    )
    use_precomputed = forms.BooleanField(
        required=False,
        label="Or, use precomputed?"
    )


class NodesForm(forms.Form):

    method = forms.ChoiceField(
        required=True,
        choices=ALGO_CHOICES2,
        label="Which algorithm to use?"
    )
    how_many = forms.IntegerField(
        required=True,
        initial=1,
        min_value=1,
        label="How many nodes to add?"
    )
    use_real_data = forms.BooleanField(
        required=False,
        initial=True,
        label="Use Real Data?*"
    )
    evaluate = forms.BooleanField(
        required=False,
        label="Keep track of this cluster evaluation?"
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
