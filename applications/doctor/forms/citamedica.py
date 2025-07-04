from django import forms
from django.forms import ModelForm
from applications.doctor.models import CitaMedica, HorarioAtencion
from datetime import datetime, time, timedelta

class CitaMedicaForm(ModelForm):
    class Meta:
        model = CitaMedica
        fields = [
            "paciente" ,
            "fecha",
            "hora_cita",
            "estado",
            "observaciones" ,
        ]
        widgets = {
    "paciente": forms.Select(attrs={
        "class": "form-select block w-full px-4 py-2 text-sm text-gray-700 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:text-gray-200 dark:border-gray-600"
    }),
    "hora_cita": forms.Select(attrs={
        "class": "form-select block w-full px-4 py-2 text-sm text-gray-700 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:text-gray-200 dark:border-gray-600"
    }),
    "estado": forms.Select(attrs={
        "class": "form-select block w-full px-4 py-2 text-sm text-gray-700 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 dark:bg-gray-800 dark:text-gray-200 dark:border-gray-600"
    }),
    "observaciones": forms.Textarea(attrs={
        "class": "form-textarea block w-full px-4 py-2 text-sm text-gray-700 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-800 dark:text-gray-200 dark:border-gray-600",
        "rows": 4,
        "placeholder": "Escriba observaciones adicionales aquí..."
    }),
}

        labels = {
            "paciente": "Paciente",
            "fecha": "Fecha de la Cita",
            "hora_cita": "Hora de la Cita",
            "estado": "Estado de la Cita",
            "observaciones": "Observaciones",
        }

def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.fields['hora_cita'] = forms.ChoiceField(
        choices=[],
        required=True,
        label='Hora de la Cita',
        widget=forms.Select(attrs={
            "class": "form-select w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200"
        })
    )

    # Obtener la fecha desde self.data o self.instance
    fecha_str = self.data.get('fecha') or (self.instance.fecha.strftime('%Y-%m-%d') if self.instance and self.instance.fecha else None)

    if fecha_str:
        try:
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            dia_semana = fecha_obj.isoweekday()  # 1 = Lunes ... 7 = Domingo

            horarios = HorarioAtencion.objects.filter(activo=True)
            opciones = []

            for h in horarios:
                if str(dia_semana) in h.dia_semana:
                    hora_actual = datetime.combine(fecha_obj, h.hora_inicio)
                    hora_fin = datetime.combine(fecha_obj, h.hora_fin)
                    while hora_actual < hora_fin:
                        hora = hora_actual.time()
                        if not (hora >= time(12, 0) and hora < time(13, 0)):
                            hora_str = hora_actual.strftime('%H:%M')
                            opciones.append((hora_str, hora_str))
                        hora_actual += timedelta(minutes=30)

            self.fields['hora_cita'].choices = opciones

        except Exception:
            pass

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora_str = cleaned_data.get('hora_cita')

        if fecha and hora_str:
            dia_semana = fecha.isoweekday()
            try:
                hora = datetime.strptime(hora_str, '%H:%M').time()
            except ValueError:
                raise forms.ValidationError("Formato de hora inválido.")

            horarios = HorarioAtencion.objects.filter(activo=True)
            valido = False

            for horario in horarios:
                if str(dia_semana) in horario.dia_semana:
                    if horario.hora_inicio <= hora < horario.hora_fin:
                        if not (time(12, 0) <= hora < time(13, 0)):
                            valido = True
                            break

            if not valido:
                raise forms.ValidationError(
                    "La hora seleccionada no está dentro del horario permitido o está en el rango de almuerzo."
                )