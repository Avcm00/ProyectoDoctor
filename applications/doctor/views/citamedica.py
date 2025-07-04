from datetime import datetime, timedelta
import re
from time import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from applications.doctor.forms.citamedica import CitaMedicaForm
from applications.doctor.models import CitaMedica, HorarioAtencion
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,View
from django.db.models import Q


from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import JsonResponse
from applications.doctor.models import CitaMedica, HorarioAtencion

class CitaMedicaListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/citamedica/list.html'
    model = CitaMedica 
    context_object_name = 'citamedicas'
    permission_required = 'view_citamedica'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        query = Q()  # Inicializar query vacía
        if q1:
            # Corregir nombres de campos - usar los campos correctos del modelo
            query |= Q(paciente__nombres__icontains=q1) | Q(paciente__apellidos__icontains=q1)
        return self.model.objects.filter(query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:citamedicas_create')  # Corregir URL
        return context


class CitaMedicaCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = CitaMedica
    template_name = 'doctor/citamedica/form.html'
    form_class = CitaMedicaForm
    success_url = reverse_lazy('doctor:citamedicas_list')
    permission_required = 'add_citamedica'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Agregar **kwargs
        context['grabar'] = 'Grabar CitaMedica'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        citamedica = self.object
        messages.success(self.request, f"Éxito al crear la cita médica para {citamedica.paciente}.")
        return response


class CitaMedicaUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = CitaMedica
    template_name = 'doctor/citamedica/form.html'
    form_class = CitaMedicaForm
    success_url = reverse_lazy('doctor:citamedicas_list')
    permission_required = 'change_citamedica'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Agregar **kwargs
        context['grabar'] = 'Actualizar CitaMedica'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        citamedica = self.object
        messages.success(self.request, f"Éxito al actualizar la cita médica para {citamedica.paciente}.")
        return response


class CitaMedicaDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = CitaMedica
    success_url = reverse_lazy('doctor:citamedicas_list')
    permission_required = 'delete_citamedica'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Agregar **kwargs
        context['grabar'] = 'Eliminar CitaMedica'
        context['description'] = f"¿Desea eliminar la cita médica: {self.object.paciente}?"
        context['back_url'] = self.success_url
        return context
    
    def delete(self, request, *args, **kwargs):
        # Guardar info antes de eliminar
        citamedica_name = self.get_object().paciente
        
        # Llamar al delete del padre
        response = super().delete(request, *args, **kwargs)
        
        # Agregar mensaje
        messages.success(self.request, f"Éxito al eliminar la cita médica de {citamedica_name}.")
        
        return response


# APIs para el calendario
def api_citas_medicas(request):
    citas = CitaMedica.objects.all()
    eventos = []
    for cita in citas:
        eventos.append({
            "title": f"{cita.paciente.nombres} {cita.paciente.apellidos}",
            "start": f"{cita.fecha}T{cita.hora_cita}",
            "color": "#2563EB" if hasattr(cita, 'estado') and cita.estado == "AG" else "#F97316",
        })
    return JsonResponse(eventos, safe=False)


def api_dias_disponibles(request):
    """
    Devuelve una lista de números (1-7) de los días habilitados en el HorarioAtencion.
    """
    dias = set()
    horarios = HorarioAtencion.objects.filter(activo=True)
    for horario in horarios:
        dias.update(map(int, horario.dia_semana))  # convierte ['1', '2'] a [1, 2]
    dias_ordenados = sorted(dias)
    return JsonResponse(dias_ordenados, safe=False)


def api_horarios_detalle(request):
    """
    Devuelve los horarios activos por día.
    """
    data = []
    horarios = HorarioAtencion.objects.filter(activo=True)
    for h in horarios:
        for dia in h.dia_semana:
            data.append({
                'dia': int(dia),  # 1-7
                'inicio': h.hora_inicio.strftime('%H:%M'),
                'fin': h.hora_fin.strftime('%H:%M'),
            })
    return JsonResponse(data, safe=False)