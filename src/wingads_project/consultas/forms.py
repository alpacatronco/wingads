from django import forms
from .models import Consulta
from django.contrib.auth.forms import UserCreationForm

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['tipo', 'descripcion'] # Campos que el usuario llenará
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe tu consulta de marketing digital...'})
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',) 