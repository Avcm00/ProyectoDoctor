import re
from django import forms
from django.forms import ModelForm

from applications.doctor.models import ServiciosAdicionales

class ServiciosAdicionalesForm(ModelForm):
    class Meta:
        model = ServiciosAdicionales
        fields = [
            "nombre_servicio",
            "costo_servicio", 
            "descripcion", 
            "activo"         
        ]
        error_messages = {
          
            "nombre_servicio": {
                "unique": "Ya existe un servicio con este nombre.",
            },
        }
        widgets = {
            "nombre_servicio": forms.TextInput(attrs={
                "placeholder": "Ingrese el nombre del servicio",
                "id": "id_nombre_servicio",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
          
            "costo_servicio": forms.NumberInput(attrs={
                "placeholder": "Costo del servicio",
                "id": "id_costo_servicio",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),

            "descripcion": forms.Textarea(attrs={
                "placeholder": "Ingrese una descripción del servicio",
                "id": "id_descripcion",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "rows": 3,
            }),

            "activo": forms.CheckboxInput(attrs={
                "id": "id_activo",
                "class": "form-check-input",
            }),
        }
        labels = {
            "nombre_servicio": "Nombre de Servicio",
            "costo_servicio": "Costo del Servicio", 
            "descripcion" : "Descripción",
            "activo": "Activo"          
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