from django import forms
from .models import Home

class HomeForm(forms.ModelForm):
    class Meta:
        model = Home
        fields = ['home_address', 'home_sqft', 'home_bedrooms', 'home_bathrooms', 'home_acquired', 'home_photo']
        widgets = {
            'home_acquired': forms.DateInput(
                format=('%m-%d-%Y'),
                attrs={
                    'placeholder': 'When did you move in?',
                    'type': 'date'
                }
            ),
        }