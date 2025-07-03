from django.contrib import messages
from django.urls import reverse_lazy
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from applications.core.models import GastoMensual
from applications.core.forms.gastomensual import GastoMensualForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

class GastoMensualListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/gastomensuals/list.html'
    model = GastoMensual
    context_object_name = 'gastomensuals'
    permission_required = 'view_gastomensual'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(name__icontains=q1), Q.OR)
           
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:gastomensual_create')
        print(context['permissions'])
        return context

class GastoMensualCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = GastoMensual
    template_name = 'core/gastomensuals/form.html'
    form_class = GastoMensualForm
    success_url = reverse_lazy('core:gastomensual_list')
    permission_required = 'add_gastomensual'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar GastoMensual'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        gastomensual = self.object
        messages.success(self.request, f"Éxito al crear el gastomensual {gastomensual.tipo_gasto}.")
        return response

class GastoMensualUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = GastoMensual
    template_name = 'core/gastomensuals/form.html'
    form_class = GastoMensualForm
    success_url = reverse_lazy('core:gastomensual_list')
    permission_required = 'change_gastomensual'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar GastoMensual'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        gastomensual = self.object
        messages.success(self.request, f"Éxito al actualizar el gastomensual {gastomensual.tipo_gasto}.")
        return response

class GastoMensualDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = GastoMensual
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:gastomensual_list')
    permission_required = 'delete_gastomensual'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar GastoMensual'
        context['description'] = f"¿Desea eliminar el gastomensual: {self.object.name}?"
        context['back_url'] = self.success_url
        return context

    
    def form_valid(self, form):
        # Guardar info antes de eliminar
        gastomensual_name = self.object.nombre
        
        # Llamar al delete del padre
        response = super().form_valid(form)
        
        # Agregar mensaje
        messages.success(self.request, f"Éxito al eliminar lógicamente el gastomensual {gastomensual_name}.")
        
        return response