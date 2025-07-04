from django import forms
from .models import CitaMedica
from applications.core.models import Paciente
from django.core.exceptions import ValidationError
from .models import CitaMedica, HorarioAtencion
from django.utils import timezone
from datetime import datetime, timedelta
from .models import CitaMedica, HorarioAtencion


class CitaMedicaForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        # Extraer fecha seleccionada si se pasa
        self.fecha_seleccionada = kwargs.pop('fecha_seleccionada', None)
        super().__init__(*args, **kwargs)
        
        # Configurar widgets con clases CSS
        self.fields['fecha'].widget = forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'id': 'id_fecha'
        })
        
        self.fields['hora_cita'].widget = forms.Select(attrs={
            'class': 'form-control w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'id': 'id_hora_cita'
        })
        
        # Configurar otros campos
        self.fields['paciente'].widget.attrs.update({
            'class': 'form-control w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'
        })
        self.fields['estado'].widget.attrs.update({
            'class': 'form-control w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'
        })
        self.fields['observaciones'].widget.attrs.update({
            'class': 'form-control w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'rows': 3
        })

        # Configurar choices para hora_cita basado en fecha seleccionada
        self.setup_hora_choices()

    def setup_hora_choices(self):
        """
        Configura las opciones de hora basado en la fecha seleccionada
        """
        if self.fecha_seleccionada:
            horas_disponibles = self.get_horas_disponibles(self.fecha_seleccionada)
            if horas_disponibles:
                choices = [('', 'Seleccione una hora')]
                choices.extend([(hora['value'], hora['display']) for hora in horas_disponibles])
                self.fields['hora_cita'].choices = choices
            else:
                self.fields['hora_cita'].choices = [('', 'No hay horarios disponibles para esta fecha')]
        else:
            self.fields['hora_cita'].choices = [('', 'Seleccione una fecha primero')]

    def get_horas_disponibles(self, fecha):
        """
        Obtiene las horas disponibles para una fecha específica
        """
        if not fecha:
            return []
            
        # Obtener el día de la semana (0=lunes, 6=domingo)
        dia_semana = fecha.weekday()
        
        # Buscar horarios de atención activos para ese día
        horarios = HorarioAtencion.objects.filter(
            activo=True,
            dia_semana__contains=str(dia_semana)
        )
        
        if not horarios.exists():
            return []
        
        horas_disponibles = []
        
        # Generar horas cada 30 minutos
        for horario in horarios:
            try:
                # Convertir horas a minutos para facilitar cálculos
                hora_inicio_minutos = horario.hora_inicio.hour * 60 + horario.hora_inicio.minute
                hora_fin_minutos = horario.hora_fin.hour * 60 + horario.hora_fin.minute
                
                minutos_actual = hora_inicio_minutos
                
                while minutos_actual < hora_fin_minutos:
                    # Convertir minutos de vuelta a horas
                    horas = minutos_actual // 60
                    minutos = minutos_actual % 60
                    
                    # Verificar si está en el intervalo de descanso
                    if horario.intervalo_desde and horario.intervalo_hasta:
                        intervalo_desde_minutos = horario.intervalo_desde.hour * 60 + horario.intervalo_desde.minute
                        intervalo_hasta_minutos = horario.intervalo_hasta.hour * 60 + horario.intervalo_hasta.minute
                        
                        if intervalo_desde_minutos <= minutos_actual < intervalo_hasta_minutos:
                            minutos_actual += 30
                            continue
                    
                    # Formatear hora
                    hora_str = f"{horas:02d}:{minutos:02d}"
                    
                    # Verificar si ya existe una cita en esa hora
                    cita_existente = CitaMedica.objects.filter(
                        fecha=fecha,
                        hora_cita=hora_str
                    )
                    
                    # Si estamos editando, excluir la cita actual
                    if self.instance and self.instance.pk:
                        cita_existente = cita_existente.exclude(pk=self.instance.pk)
                    
                    if not cita_existente.exists():
                        horas_disponibles.append({
                            'value': hora_str,
                            'display': hora_str
                        })
                    
                    minutos_actual += 30
                    
            except Exception as e:
                # Log del error para debugging
                print(f"Error procesando horario {horario.id}: {str(e)}")
                continue
        
        return horas_disponibles

    class Meta:
        model = CitaMedica
        fields = ['paciente', 'fecha', 'hora_cita', 'estado', 'observaciones']
        labels = {
            'paciente': 'Paciente',
            'fecha': 'Fecha de la Cita',
            'hora_cita': 'Hora de la Cita',
            'estado': 'Estado',
            'observaciones': 'Observaciones'
        }
        
    def clean_fecha(self):
        """
        Valida que la fecha no sea en el pasado
        """
        fecha = self.cleaned_data.get('fecha')
        
        if fecha:
            from django.utils import timezone
            if fecha < timezone.now().date():
                raise ValidationError("No se pueden crear citas en fechas pasadas.")
        
        return fecha
    
    def clean_hora_cita(self):
        """
        Valida que la hora esté en formato correcto
        """
        hora_cita = self.cleaned_data.get('hora_cita')
        
        if hora_cita:
            # Validar formato HH:MM usando regex
            if not re.match(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$', hora_cita):
                raise ValidationError("Formato de hora inválido. Use HH:MM")
        
        return hora_cita
        
    def clean(self):
        """
        Validación global del formulario
        """
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora_cita = cleaned_data.get('hora_cita')
        
        if fecha and hora_cita:
            # Validar horario de atención
            if not self.validar_horario_atencion(fecha, hora_cita):
                raise ValidationError("La hora seleccionada no está disponible en el horario de atención.")
            
            # Validar que no exista otra cita en la misma fecha y hora
            cita_existente = CitaMedica.objects.filter(fecha=fecha, hora_cita=hora_cita)
            
            # Si estamos editando, excluir la cita actual
            if self.instance and self.instance.pk:
                cita_existente = cita_existente.exclude(pk=self.instance.pk)
            
            if cita_existente.exists():
                raise ValidationError("Ya existe una cita programada para esta fecha y hora.")
        
        return cleaned_data
    
    def validar_horario_atencion(self, fecha, hora_cita_str):
        """
        Valida que la fecha y hora estén dentro del horario de atención
        """
        try:
            # Convertir string de hora a minutos
            horas, minutos = map(int, hora_cita_str.split(':'))
            hora_cita_minutos = horas * 60 + minutos
        except ValueError:
            return False
        
        dia_semana = fecha.weekday()
        
        # Buscar horarios de atención activos para ese día
        horarios = HorarioAtencion.objects.filter(
            activo=True,
            dia_semana__contains=str(dia_semana)
        )
        
        # Verificar si la hora está dentro de algún horario válido
        for horario in horarios:
            if self.hora_en_horario_valido(hora_cita_minutos, horario):
                return True
        
        return False
    
    def hora_en_horario_valido(self, hora_cita_minutos, horario):
        """
        Verifica si una hora está dentro del horario de atención
        """
        try:
            # Convertir horarios a minutos
            hora_inicio_minutos = horario.hora_inicio.hour * 60 + horario.hora_inicio.minute
            hora_fin_minutos = horario.hora_fin.hour * 60 + horario.hora_fin.minute
            
            # Verificar si está dentro del rango general
            if not (hora_inicio_minutos <= hora_cita_minutos <= hora_fin_minutos):
                return False
            
            # Si hay intervalo de descanso, verificar que no esté en ese rango
            if horario.intervalo_desde and horario.intervalo_hasta:
                intervalo_desde_minutos = horario.intervalo_desde.hour * 60 + horario.intervalo_desde.minute
                intervalo_hasta_minutos = horario.intervalo_hasta.hour * 60 + horario.intervalo_hasta.minute
                
                if intervalo_desde_minutos <= hora_cita_minutos < intervalo_hasta_minutos:
                    return False
            
            return True
        except Exception as e:
            # Log del error para debugging
            print(f"Error validando horario: {str(e)}")
            return False