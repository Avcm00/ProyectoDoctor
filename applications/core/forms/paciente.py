from django import forms
from django.forms import ModelForm
from applications.core.models import Paciente
from django.core.exceptions import ValidationError
from datetime import date

class PacienteForm(ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'nombres', 'apellidos', 'cedula_ecuatoriana', 'dni', 'fecha_nacimiento',
            'telefono', 'email', 'sexo', 'estado_civil', 'direccion', 'latitud', 'longitud',
            'tipo_sangre', 'foto', 'antecedentes_personales', 'antecedentes_quirurgicos',
            'antecedentes_familiares', 'alergias', 'medicamentos_actuales', 'habitos_toxicos',
            'vacunas', 'antecedentes_gineco_obstetricos', 'activo'
        ]

        widgets = {
            "nombres": forms.TextInput(attrs={
                "placeholder": " ",
                "id": "id_nombres",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white",
            }),
            "apellidos": forms.TextInput(attrs={
                "placeholder": " ",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white",
            }),
            "cedula_ecuatoriana": forms.TextInput(attrs={
                "placeholder": " ",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white",
            }),
            "dni": forms.TextInput(attrs={
                "placeholder": " ",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white",
            }),
            "fecha_nacimiento": forms.DateInput(attrs={
                "type": "date",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white",
            }),
            "telefono": forms.TextInput(attrs={
                "placeholder": " ",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white",
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": " ",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white",
            }),
            "sexo": forms.Select(attrs={
                "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white",
            }),
            "estado_civil": forms.Select(attrs={
                "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white",
            }),
            "direccion": forms.TextInput(attrs={
                "placeholder": " ",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white",
            }),
            "latitud": forms.NumberInput(attrs={
                "placeholder": " ",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white",
            }),
            "longitud": forms.NumberInput(attrs={
                "placeholder": " ",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white",
            }),
            "tipo_sangre": forms.Select(attrs={
                "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white",
            }),
            "foto": forms.FileInput(attrs={
                "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white",
            }),
            "antecedentes_personales": forms.Textarea(attrs={
                "placeholder": " ",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white",
                "rows": 3,
            }),
            "antecedentes_quirurgicos": forms.Textarea(attrs={
                "placeholder": " ",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white",
                "rows": 3,
            }),
            "antecedentes_familiares": forms.Textarea(attrs={
                "placeholder": " ",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white",
                "rows": 3,
            }),
            "alergias": forms.Textarea(attrs={
                "placeholder": " ",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white",
                "rows": 3,
            }),
            "medicamentos_actuales": forms.Textarea(attrs={
                "placeholder": " ",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white",
                "rows": 3,
            }),
            "habitos_toxicos": forms.TextInput(attrs={
                "placeholder": " ",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white",
            }),
            "vacunas": forms.Textarea(attrs={
                "placeholder": " ",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white",
                "rows": 3,
            }),
            "antecedentes_gineco_obstetricos": forms.Textarea(attrs={
                "placeholder": " ",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white",
                "rows": 3,
            }),
            "activo": forms.CheckboxInput(attrs={
                "class": "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white",
            }),
        }

        labels = {
            "cedula_ecuatoriana": "Cédula",
            "dni": "DNI Internacional",
            "fecha_nacimiento": "Fecha de Nacimiento",
            "telefono": "Teléfono(s)",
            "email": "Correo Electrónico",
            "sexo": "Sexo",
            "estado_civil": "Estado Civil",
            "tipo_sangre": "Tipo de Sangre",
            "foto": "Foto de Perfil",
            "activo": "Activo",
        }

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get("fecha_nacimiento")
        if fecha and fecha > date.today():
            raise ValidationError("La fecha de nacimiento no puede ser en el futuro.")
        return fecha

    def clean_telefono(self):
        telefono = self.cleaned_data.get("telefono")
        if not telefono:
            raise ValidationError("El campo teléfono es obligatorio.")
        return telefono

    def clean_nombres(self):
        nombres = self.cleaned_data.get("nombres")
        return nombres.upper()

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get("apellidos")
        return apellidos.upper()
