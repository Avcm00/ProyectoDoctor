from django.urls import path
from applications.core.views.pacientefind import paciente_find
from applications.core.views.tiposangre import TipoSangreCreateView, TipoSangreDeleteView, TipoSangreListView, TipoSangreUpdateView
from applications.core.views.paciente import PacienteCreateView, PacienteDeleteView, PacienteListView, PacienteUpdateView
from applications.core.views.tipogasto import TipoGastoCreateView, TipoGastoDeleteView, TipoGastoListView, TipoGastoUpdateView
from applications.core.views.gastomensual import GastoMensualCreateView, GastoMensualDeleteView, GastoMensualListView, GastoMensualUpdateView   

app_name='core' # define un espacio de nombre para la aplicacion
urlpatterns = [
    # Rutas  para vistas relacionadas con Pacientes
    path('paciente_find/', paciente_find, name="paciente_find"),

    # rutas de tiposangres
    path('tiposangre_list/',TipoSangreListView.as_view() ,name="tiposangre_list"),
    path('tiposangre_create/', TipoSangreCreateView.as_view(),name="tiposangre_create"),
    path('tiposangre_update/<int:pk>/', TipoSangreUpdateView.as_view(),name='tiposangre_update'),
    path('tiposangre_delete/<int:pk>/', TipoSangreDeleteView.as_view(),name='tiposangre_delete'),

    # rutas para tipogastos
    path('tipogasto_list/', TipoGastoListView.as_view(), name='tipogasto_list'),
    path('tipogasto_create/', TipoGastoCreateView.as_view(), name='tipogasto_create'),
    path('tipogasto_update/<int:pk>/', TipoGastoUpdateView.as_view(), name='tipogasto_update'),
    path('tipogasto_delete/<int:pk>/', TipoGastoDeleteView.as_view(), name='tipogasto_delete'),

    # rutas para gastos mensuales
    path('gastomensual_list/', GastoMensualListView.as_view(), name='gastomensual_list'),
    path('gastomensual_create/', GastoMensualCreateView.as_view(), name='gastomensual_create'),
    path('gastomensual_update/<int:pk>/', GastoMensualUpdateView.as_view(), name='gastomensual_update'),
    path('gastomensual_delete/<int:pk>/', GastoMensualDeleteView.as_view(), name='gastomensual_delete'),

    # rutas para pacientes
    path('paciente_list/', PacienteListView.as_view(), name='paciente_list'),
    path('paciente_create/', PacienteCreateView.as_view(), name='paciente_create'),
    path('paciente_update/<int:pk>/', PacienteUpdateView.as_view(), name='paciente_update'),
    path('paciente_delete/<int:pk>/', PacienteDeleteView.as_view(), name='paciente_delete'),

]