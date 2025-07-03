from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from applications.doctor.forms.citamedica import CitaMedicaForm
from applications.doctor.models import CitaMedica, HorarioAtencion
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q


class CitaMedicaListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/citamedica/list.html'
    model = CitaMedica 
    context_object_name = 'citamedicas'
    permission_required = 'view_citamedica'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(paciente__nombre__icontains=q1) | Q(paciente__apellido__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:citamedica_create')
        print(context['permissions'])
        return context

class CitaMedicaCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = CitaMedica
    template_name = 'doctor/citamedica/form.html'
    form_class = CitaMedicaForm
    success_url = reverse_lazy('doctor:citamedicas_list')
    permission_required = 'add_citamedica'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar CitaMedica'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        citamedica = self.object
        messages.success(self.request, f"Éxito al crear el citamedica {citamedica.paciente}.")
        return response

class CitaMedicaUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = CitaMedica
    template_name = 'doctor/citamedica/form.html'
    form_class = CitaMedicaForm
    success_url = reverse_lazy('doctor:citamedicas_list')
    permission_required = 'change_citamedica'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar CitaMedica'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        citamedica = self.object
        messages.success(self.request, f"Éxito al actualizar el citamedica {citamedica.paciente}.")
        return response

class CitaMedicaDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = CitaMedica
    template_name = 'doctor/delete.html'
    success_url = reverse_lazy('doctor:citamedicas_list')
    permission_required = 'delete_citamedica'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar CitaMedica'
        context['description'] = f"¿Desea eliminar el citamedica: {self.object.paciente}?"
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        # Guardar info antes de eliminar
        citamedica_name = self.object.paciente
        
        # Llamar al delete del padre
        response = super().form_valid(form)
        
        # Agregar mensaje
        messages.success(self.request, f"Éxito al eliminar lógicamente el citamedica {citamedica_name}.")
        
        return response
    
    from django.http import JsonResponse
from applications.doctor.models import CitaMedica

def api_citas_medicas(request):
    citas = CitaMedica.objects.all()
    eventos = []
    for cita in citas:
        eventos.append({
            "title": cita.paciente.nombre_completo,
            "start": f"{cita.fecha}T{cita.hora_cita}",
            "color": "#2563EB" if cita.estado == "AG" else "#F97316",
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
def get_queryset(self):
    q1 = self.request.GET.get('q')
    query = Q()
    if q1:
        query |= Q(paciente__nombre__icontains=q1) | Q(paciente__apellido__icontains=q1)
    return self.model.objects.filter(query).order_by('id')

    
from django import forms
from applications.doctor.models import CitaMedica, HorarioAtencion
from django.core.exceptions import ValidationError
    
class CitaMedicaForm(forms.ModelForm):
    class Meta:
        model = CitaMedica
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        if fecha:
                # Django: lunes=1 ... domingo=7
            dia_semana = fecha.isoweekday()
                # Buscar si hay algún horario activo para ese día
            horarios = HorarioAtencion.objects.filter(activo=True, dia_semana__contains=str(dia_semana))
            if not horarios.exists():
                raise ValidationError(f"No se puede agendar una cita para ese día. Solo se permiten días con horario de atención activo.")
            return cleaned_data
        
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