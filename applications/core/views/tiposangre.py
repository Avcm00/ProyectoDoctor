from django.contrib import messages
from django.urls import reverse_lazy
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from applications.core.models import TipoSangre
from applications.core.forms.tiposangre import TipoSangreForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q


class TipoSangreListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/tiposangres/list.html'
    model = TipoSangre
    context_object_name = 'tiposangres'
    permission_required = 'view_tiposangre'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(name__icontains=q1), Q.OR)
           
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:tiposangre_create')
        print(context['permissions'])
        return context


class TipoSangreCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = TipoSangre
    template_name = 'core/tiposangres/form.html'
    form_class = TipoSangreForm
    success_url = reverse_lazy('core:tiposangre_list')
    permission_required = 'add_tiposangre'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Tiposangre'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tiposangre = self.object
        messages.success(self.request, f"Éxito al crear el tiposangre {tiposangre.tipo}.")
        return response


class TipoSangreUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = TipoSangre
    template_name = 'core/tiposangres/form.html'
    form_class = TipoSangreForm
    success_url = reverse_lazy('core:tiposangre_list')
    permission_required = 'change_tiposangre'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Tiposangre'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tiposangre = self.object
        messages.success(self.request, f"Éxito al actualizar el tiposangre {tiposangre.tipo}.")
        return response


class TipoSangreDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = TipoSangre
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:tiposangre_list')
    permission_required = 'delete_tiposangre'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Tiposangre'
        context['description'] = f"¿Desea eliminar el tiposangre: {self.object.name}?"
        context['back_url'] = self.success_url
        return context

    
    def form_valid(self, form):
        # Guardar info antes de eliminar
        tiposangre_name = self.object.tipo
        
        # Llamar al delete del padre
        response = super().form_valid(form)
        
        # Agregar mensaje
        messages.success(self.request, f"Éxito al eliminar lógicamente el tiposangre {tiposangre_name}.")
        
        return response