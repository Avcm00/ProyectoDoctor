from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from applications.doctor.models import HorarioAtencion
from applications.doctor.forms.horarioatencion import HorarioAtencionForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

class HorarioAtencionListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/horarioatenciones/list.html'
    model = HorarioAtencion
    context_object_name = 'horarioatenciones'
    permission_required = 'view_horarioatencion'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(name__icontains=q1), Q.OR)
           
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:horarioatenciones_create')
        context['mostrar_boton'] = not HorarioAtencion.objects.exists()  # Solo mostrar si no hay registros
        return context

class HorarioAtencionCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = HorarioAtencion
    template_name = 'doctor/horarioatenciones/form.html'
    form_class = HorarioAtencionForm
    success_url = reverse_lazy('doctor:horarioatenciones_list')
    permission_required = 'add_horarioatencion'

    def dispatch(self, request, *args, **kwargs):
        # Bloquear creación si ya existe un horario
        if HorarioAtencion.objects.exists():
            messages.warning(self.request, "Ya existe un horario registrado. No puede crear otro.")
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Horarioatenciones'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        horarioatenciones = self.object
        messages.success(self.request, f"Éxito al crear el horarioatenciones {horarioatenciones.dia_semana}.")
        return response

class HorarioAtencionUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = HorarioAtencion
    template_name = 'doctor/horarioatenciones/form.html'
    form_class = HorarioAtencionForm
    success_url = reverse_lazy('doctor:horarioatenciones_list')
    permission_required = 'change_horarioatencion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Horarioatenciones'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        horarioatenciones = self.object
        messages.success(self.request, f"Éxito al actualizar el horarioatenciones {horarioatenciones.dia_semana}.")
        return response

class HorarioAtencionDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = HorarioAtencion
    template_name = 'doctor/delete.html'
    success_url = reverse_lazy('doctor:horarioatenciones_list')
    permission_required = 'delete_horarioatencion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Horarioatenciones'
        context['description'] = f"¿Desea eliminar el horarioatenciones: {self.object.dia_semana}?"
        context['back_url'] = self.success_url
        return context

    
    def form_valid(self, form):
        # Guardar info antes de eliminar
        horarioatenciones_name = self.object.dia_semana
        
        # Llamar al delete del padre
        response = super().form_valid(form)
        
        # Agregar mensaje
        messages.success(self.request, f"Éxito al eliminar lógicamente el horarioatenciones {horarioatenciones_name}.")
        
        return response
    
