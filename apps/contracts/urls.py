from django.urls import path
from . import views

app_name = 'contracts'
urlpatterns = [
    path('', views.ContractListView.as_view(), name='contract_list'),
    path('add/', views.ContractCreateView.as_view(), name='contract_add'),
    path('<int:pk>/', views.ContractDetailView.as_view(), name='contract_detail'),
    path('<int:pk>/edit/', views.ContractUpdateView.as_view(), name='contract_edit'),
    path('<int:pk>/delete/', views.ContractDeleteView.as_view(), name='contract_delete'),
]