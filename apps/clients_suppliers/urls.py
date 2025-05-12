from django.urls import path
from . import views

app_name = 'clients_suppliers'

urlpatterns = [
    # Party CRUD
    path('', views.PartyListView.as_view(), name='party_list'),
    path('add/', views.PartyCreateView.as_view(), name='party_add'),
    path('<int:pk>/', views.PartyDetailView.as_view(), name='party_detail'),
    path('<int:pk>/edit/', views.PartyUpdateView.as_view(), name='party_edit'),
    path('<int:pk>/delete/', views.PartyDeleteView.as_view(), name='party_delete'),
    # Contact CRUD (nested under Party)
    path('<int:party_pk>/contacts/add/', views.ContactCreateView.as_view(), name='contact_add'),
    path('<int:party_pk>/contacts/<int:pk>/edit/', views.ContactUpdateView.as_view(), name='contact_edit'),
    path('<int:party_pk>/contacts/<int:pk>/delete/', views.ContactDeleteView.as_view(), name='contact_delete'),
]