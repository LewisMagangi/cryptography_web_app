from django import forms
from .models import FileAnalysis  # Keep this import
from .constants import *

class AlgorithmChoices:
    @staticmethod
    def get_crypto_choices():
        return [(t.value, t.name.title()) for t in CryptoType]  # Will now include 'hash' option
    
    @staticmethod
    def get_asymmetric_choices():
        return [(a.value, a.name) for a in AsymmetricAlgo]
    
    @staticmethod
    def get_symmetric_choices():
        return [(s.value, s.name) for s in SymmetricAlgo]

    @staticmethod
    def get_hash_choices():
        return [(algo.value, algo.value.upper()) for algo in HashingAlgo]  # Use the enum instead of hardcoded values

class AnalysisForm(forms.ModelForm):
    ANALYSIS_CHOICES = [
        ('keysize', 'Key Size Analysis'),
        ('filesize', 'File Size Analysis')
    ]

    class Meta:
        model = FileAnalysis
        fields = ['crypto_type', 'algorithm', 'analysis_type']  # Reorder fields

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

    analysis_type = forms.ChoiceField(
        choices=ANALYSIS_CHOICES,
        initial='filesize',
        widget=forms.Select(attrs={'class': 'form-control'}),  # Changed to Select widget
        label='Analysis Type'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial choices based on crypto type
        if self.data.get('crypto_type') == 'symmetric':
            self.fields['algorithm'].choices = AlgorithmChoices.get_symmetric_choices()
        elif self.data.get('crypto_type') == 'asymmetric':
            self.fields['algorithm'].choices = AlgorithmChoices.get_asymmetric_choices()
        else:  # hash type
            self.fields['algorithm'].choices = AlgorithmChoices.get_hash_choices()

    def clean(self):
        cleaned_data = super().clean()
        crypto_type = cleaned_data.get('crypto_type')
        algorithm = cleaned_data.get('algorithm')
        analysis_type = cleaned_data.get('analysis_type')
        
        # Store analysis type in metric field
        cleaned_data['metric'] = analysis_type

        if crypto_type == 'hash':
            # Convert to lowercase for hash algorithms
            algorithm = algorithm.lower() if algorithm else None
            cleaned_data['algorithm'] = algorithm

        if crypto_type and algorithm:
            if crypto_type == 'symmetric':
                valid_choices = AlgorithmChoices.get_symmetric_choices()
            elif crypto_type == 'asymmetric':
                valid_choices = AlgorithmChoices.get_asymmetric_choices()
            else:
                valid_choices = AlgorithmChoices.get_hash_choices()
            
            valid_values = [choice[0] for choice in valid_choices]
            if algorithm not in valid_values:
                self.add_error('algorithm', 'Invalid algorithm choice for selected cryptography type')

        return cleaned_data
