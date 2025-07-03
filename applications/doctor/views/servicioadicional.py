from django.contrib import messages
from django.urls import reverse_lazy
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from applications.doctor.models import ServiciosAdicionales
from applications.doctor.forms.servicioadicional import ServiciosAdicionalesForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

class ServicioAdicionalesListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/serviciosadicionaless/list.html'
    model = ServiciosAdicionales
    context_object_name = 'serviciosadicionales'
    permission_required = 'view_serviciosadicionales'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(name__icontains=q1), Q.OR)
           
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:serviciosadicionales_create')
        print(context['permissions'])
        return context

class ServicioAdicionalesCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = ServiciosAdicionales
    template_name = 'doctor/serviciosadicionaless/form.html'
    form_class = ServiciosAdicionalesForm
    success_url = reverse_lazy('doctor:serviciosadicionales_list')
    permission_required = 'add_serviciosadicionales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Serviciosadicionales'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        serviciosadicionales = self.object
        messages.success(self.request, f"Éxito al crear el serviciosadicionales {serviciosadicionales.nombre_servicio}.")
        return response

class ServicioAdicionalesUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = ServiciosAdicionales
    template_name = 'doctor/serviciosadicionaless/form.html'
    form_class = ServiciosAdicionalesForm
    success_url = reverse_lazy('doctor:serviciosadicionales_list')
    permission_required = 'change_serviciosadicionales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Serviciosadicionales'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        serviciosadicionales = self.object
        messages.success(self.request, f"Éxito al actualizar el serviciosadicionales {serviciosadicionales.nombre_servicio}.")
        return response

class ServicioAdicionalesDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = ServiciosAdicionales
    template_name = 'doctor/delete.html'
    success_url = reverse_lazy('doctor:serviciosadicionales_list')
    permission_required = 'delete_serviciosadicionales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Serviciosadicionales'
        context['description'] = f"¿Desea eliminar el serviciosadicionales: {self.object.nombre_servicio}?"
        context['back_url'] = self.success_url
        return context

    
    def form_valid(self, form):
        # Guardar info antes de eliminar
        serviciosadicionales_name = self.object.nombre_servicio
        
        # Llamar al delete del padre
        response = super().form_valid(form)
        
        # Agregar mensaje
        messages.success(self.request, f"Éxito al eliminar lógicamente el serviciosadicionales {serviciosadicionales_name}.")
        
        return response