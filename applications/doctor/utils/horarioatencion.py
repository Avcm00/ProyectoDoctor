from applications.doctor.models import HorarioAtencion

def obtener_dias_habilitados():
    horario = HorarioAtencion.objects.first()
    return horario.dia_semana if horario else []
def obtener_horas_habilitadas():
    horario = HorarioAtencion.objects.first()
    if horario:
        return {
            'hora_inicio': horario.hora_inicio,
            'hora_fin': horario.hora_fin,
            'intervalo_desde': horario.intervalo_desde,
            'intervalo_hasta': horario.intervalo_hasta
        }
    return {}