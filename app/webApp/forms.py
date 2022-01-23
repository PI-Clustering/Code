from django import forms
# from .models import Document


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


DATASET_CHOICES = [
    ('ldbc', 'LDBC'),
    ('covid-19', 'Covid 19'),
]


class TimerForm(forms.Form):
    algo = forms.CharField(label='Algo', max_length=20)
    dataset = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=DATASET_CHOICES,
    )
