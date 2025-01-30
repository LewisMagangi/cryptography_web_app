from django import forms
from .constants import *

class AlgorithmChoices:
    @staticmethod
    def get_crypto_choices():
        return [(t.value, t.name.title()) for t in CryptoType]
    
    @staticmethod
    def get_asymmetric_choices():
        return [(a.value, a.name) for a in AsymmetricAlgo]
    
    @staticmethod
    def get_symmetric_choices():
        return [(s.value, s.name) for s in SymmetricAlgo]

class AnalysisForm(forms.Form):
    crypto_type = forms.ChoiceField(
        choices=AlgorithmChoices.get_crypto_choices(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Cryptography Type'
    )

    algorithm = forms.ChoiceField(
        choices=[],  # Will be populated dynamically
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Algorithm'
    )

    metric = forms.ChoiceField(
        choices=[(t.value, t.name.replace('_', ' ').title()) for t in MetricType],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Analysis Metric'
    )

    visualization = forms.ChoiceField(
        choices=[(t.value, t.name.title()) for t in VisualizationType],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Visualization Type'
    )

    bar_type = forms.ChoiceField(
        choices=[(t.value, t.name.title()) for t in BarChartType],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Bar Chart Type',
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial choices
        if self.data.get('crypto_type') == 'symmetric':
            self.fields['algorithm'].choices = AlgorithmChoices.get_symmetric_choices()
        else:
            self.fields['algorithm'].choices = AlgorithmChoices.get_asymmetric_choices()

    def clean(self):
        cleaned_data = super().clean()
        crypto_type = cleaned_data.get('crypto_type')
        algorithm = cleaned_data.get('algorithm')

        if crypto_type and algorithm:
            valid_choices = (AlgorithmChoices.get_symmetric_choices() 
                           if crypto_type == 'symmetric' 
                           else AlgorithmChoices.get_asymmetric_choices())
            
            valid_values = [choice[0] for choice in valid_choices]
            if algorithm not in valid_values:
                self.add_error('algorithm', 'Invalid algorithm choice for selected cryptography type')

        return cleaned_data
