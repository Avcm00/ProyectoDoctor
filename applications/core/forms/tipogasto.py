import re
from django import forms
from django.forms import ModelForm

from applications.core.models import TipoGasto

class TipoGastoForm(ModelForm):
    class Meta:
        model = TipoGasto
        fields = [
            "nombre",
            "descripcion", 
            "activo",          
        ]
        error_messages = {
          
            "nombre": {
                "unique": "Ya existe un nombre de tipo de gasto con este nombre.",
            },
        }
        widgets = {
            "nombre": forms.TextInput(attrs={
                "placeholder": "Ingrese el tipo de gasto",
                "id": "id_tipo",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
          
            "descripcion": forms.TextInput(attrs={
                "placeholder": "Desripcion del tipo de gasto",
                "id": "id_descripcion",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "activo": forms.CheckboxInput(attrs={
                "id": "id_activo",
                "class": "form-check-input",
            }),
        }
        labels = {
            "nombre": "Nombre de Gasto",
            "descripcion": "Descripcion", 
            "gasto" : "Gasto",          
        }

    def clean_name(self):
        name = self.cleaned_data.get("tipo")
        return name.upper()
    
    def clean_icon(self):
        icon = self.cleaned_data['descripcion']
        if not icon:
            raise forms.ValidationError("El campo descripcion es requerido.")
        
        # Patrones para FontAwesome v5 y v6
        patterns = [
            r'^(fas|far|fal|fad|fab|fa)\s+fa-\w+',      # fas fa-user (v5)
            r'^fa-(solid|regular|light|duotone|brands)\s+fa-\w+',  # fa-solid fa-user (v6)
            r'^fa-\w+$',                                 # fa-user (formato simple)
        ]
        
        is_valid = any(re.match(pattern, icon) for pattern in patterns)
        
        if not is_valid:
            raise forms.ValidationError(
                "Formato de ícono inválido. Ejemplos válidos: "
                "'fas fa-user', 'fa-solid fa-person', 'fa-home'"
            )
        
        return icon