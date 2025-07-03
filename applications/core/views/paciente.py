from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from applications.security.components.mixin_crud import (
    CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
)
from applications.core.models import Paciente
from applications.core.forms.paciente import PacienteForm


class PacienteListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/pacientes/list.html'
    model = Paciente
    context_object_name = 'pacientes'
    permission_required = 'view_paciente'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(
                Q(nombres__icontains=q1) | Q(apellidos__icontains=q1) | Q(cedula_ecuatoriana__icontains=q1),
                Q.AND
            )
        return self.model.objects.filter(self.query).order_by('apellidos', 'nombres')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:paciente_create')
        print(context['permissions'])
        return context


class PacienteCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Paciente
    template_name = 'core/pacientes/form.html'
    form_class = PacienteForm
    success_url = reverse_lazy('core:paciente_list')
    permission_required = 'add_paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Paciente'
        context['back_url'] = self.success_url
        context["campos_info_personal"] = [
        "nombres", "apellidos", "cedula_ecuatoriana", "dni", "fecha_nacimiento",
        "telefono", "email", "sexo", "estado_civil", "tipo_sangre"
        ]
        context["campos_contacto"] = [
        "direccion", "latitud", "longitud", "foto"
        ]
        context["campos_historia_medica"] = [
        "antecedentes_personales", "antecedentes_familiares", "antecedentes_quirurgicos",
        "alergias", "medicamentos_actuales", "habitos_toxicos", "vacunas",
        "antecedentes_gineco_obstreticos"
        ]
        context["campos_estado"] = [
        "activo"
        ]
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        paciente = self.object
        messages.success(self.request, f"Éxito al crear el paciente {paciente.nombre_completo}.")
        return response


class PacienteUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Paciente
    template_name = 'core/pacientes/form.html'
    form_class = PacienteForm
    success_url = reverse_lazy('core:paciente_list')
    permission_required = 'change_paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Paciente'
        context['back_url'] = self.success_url
        context["campos_info_personal"] = [
        "nombres", "apellidos", "cedula_ecuatoriana", "dni", "fecha_nacimiento",
        "telefono", "email", "sexo", "estado_civil", "tipo_sangre"
        ]
        context["campos_contacto"] = [
        "direccion", "latitud", "longitud", "foto"
        ]
        context["campos_historia_medica"] = [
        "antecedentes_personales", "antecedentes_familiares", "antecedentes_quirurgicos",
        "alergias", "medicamentos_actuales", "habitos_toxicos", "vacunas",
        "antecedentes_gineco_obstreticos"
        ]
        context["campos_estado"] = [
        "activo"
        ]
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        paciente = self.object
        messages.success(self.request, f"Éxito al actualizar el paciente {paciente.nombre_completo}.")
        return response


class PacienteDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Paciente
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:paciente_list')
    permission_required = 'delete_paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Paciente'
        context['description'] = f"¿Desea eliminar el paciente: {self.object.nombre_completo}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        paciente_name = self.object.nombre_completo
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al eliminar lógicamente el paciente {paciente_name}.")
        return response
