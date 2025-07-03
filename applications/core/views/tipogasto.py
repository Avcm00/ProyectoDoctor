from django.contrib import messages
from django.urls import reverse_lazy
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from applications.core.models import TipoGasto
from applications.core.forms.tipogasto import TipoGastoForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

class TipoGastoListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/tipogastos/list.html'
    model = TipoGasto
    context_object_name = 'tipogastos'
    permission_required = 'view_tipogasto'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(name__icontains=q1), Q.OR)
           
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:tipogasto_create')
        print(context['permissions'])
        return context

class TipoGastoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = TipoGasto
    template_name = 'core/tipogastos/form.html'
    form_class = TipoGastoForm
    success_url = reverse_lazy('core:tipogasto_list')
    permission_required = 'add_tipogasto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar TipoGasto'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tipogasto = self.object
        messages.success(self.request, f"Éxito al crear el tipogasto {tipogasto.nombre}.")
        return response

class TipoGastoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = TipoGasto
    template_name = 'core/tipogastos/form.html'
    form_class = TipoGastoForm
    success_url = reverse_lazy('core:tipogasto_list')
    permission_required = 'change_tipogasto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar TipoGasto'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tipogasto = self.object
        messages.success(self.request, f"Éxito al actualizar el tipogasto {tipogasto.nombre}.")
        return response

class TipoGastoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = TipoGasto
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:tipogasto_list')
    permission_required = 'delete_tipogasto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar TipoGasto'
        context['description'] = f"¿Desea eliminar el tipogasto: {self.object.name}?"
        context['back_url'] = self.success_url
        return context

    
    def form_valid(self, form):
        # Guardar info antes de eliminar
        tipogasto_name = self.object.nombre
        
        # Llamar al delete del padre
        response = super().form_valid(form)
        
        # Agregar mensaje
        messages.success(self.request, f"Éxito al eliminar lógicamente el tipogasto {tipogasto_name}.")
        
        return response