from django import forms
from .models import MealBooking

class MealBookingForm(forms.ModelForm):
    class Meta:
        model = MealBooking
        fields = ['date_from', 'date_to', 'breakfast', 'lunch', 'dinner']
        widgets = {
            'date_from': forms.DateInput(attrs={'type': 'date'}),
            'date_to': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')

        if date_from and date_to and date_to < date_from:
            raise forms.ValidationError("The 'To' date cannot be before the 'From' date.")
        return cleaned_data
