import re
from django import forms
from django.forms import ModelForm
from applications.doctor.models import HorarioAtencion

class HorarioAtencionForm(ModelForm):
    class Meta:
        model = HorarioAtencion
        fields = [
            "dia_semana",
            "hora_inicio", 
            "hora_fin", 
            "intervalo_desde",
            "intervalo_hasta",
            "activo",        
        ]

        widgets = {
            "dia_semana": forms.CheckboxSelectMultiple(attrs={
                "placeholder": "Seleccione un día de la semana",
                "id": "id_dia_semana",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light text-blue-500 space-x-2",
            }),

            "hora_inicio": forms.TimeInput(attrs={
                "type": "time",
                "placeholder": "Ingrese la hora de inicio",
                "id": "id_hora_inicio",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),

            "hora_fin": forms.TimeInput(attrs={
                "type": "time",
                "placeholder": "Ingrese la hora de fin",
                "id": "id_hora_fin",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),

            "intervalo_desde": forms.TimeInput(attrs={
                "type": "time",
                "placeholder": "Ingrese el intervalo desde",
                "id": "id_intervalo_desde",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),

            "intervalo_hasta": forms.TimeInput(attrs={
                "type": "time",
                "placeholder": "Ingrese el intervalo hasta",
                "id": "id_intervalo_hasta",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),

            "activo": forms.CheckboxInput(attrs={
                "id": "id_activo",
                "class": "form-check-input rounded border-gray-300 text-blue-600 shadow-sm focus:ring focus:ring-blue-500 focus:ring-opacity-50",
            }),
        }

        labels = {
            "dia_semana": "Día de la Semana",
            "hora_inicio": "Hora de Inicio", 
            "hora_fin": "Hora de Fin",
            "intervalo_desde": "Intervalo Desde",
            "intervalo_hasta": "Intervalo Hasta",
            "activo": "Activo",
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