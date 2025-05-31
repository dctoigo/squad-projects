from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import (
    ProfileUpdateView,
    BillingTypeCreateModalView,
    PaymentIntervalCreateModalView,
    ServiceTypeCreateModalView,
    TechnologyCreateModalView,
    PartyCreateModalView,
    billingtype_select_options,
    paymentinterval_select_options,
    servicetype_select_options,
    technology_select_options,
    DashboardExecutiveView,
    ClientDashboardView
)

app_name = 'manager'

urlpatterns = [
    # Auth
    path('login/', auth_views.LoginView.as_view(
            template_name='manager/login.html'
        ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
            template_name='manager/password_change.html',
            success_url=reverse_lazy('manager:password_change_done')
        ), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
            template_name='manager/password_change_done.html'
        ), name='password_change_done'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),

    # HTMX Modals for lookups
    path('billingtype/add/', BillingTypeCreateModalView.as_view(), name='billingtype_add_modal'),
    path('billingtype/select-options/', billingtype_select_options, name='billingtype_select_options'),

    path('paymentinterval/add/', PaymentIntervalCreateModalView.as_view(), name='paymentinterval_add_modal'),
    path('paymentinterval/select-options/', paymentinterval_select_options, name='paymentinterval_select_options'),

    path('servicetype/add/', ServiceTypeCreateModalView.as_view(), name='servicetype_add_modal'),
    path('servicetype/select-options/', servicetype_select_options, name='servicetype_select_options'),

    path('technology/add/', TechnologyCreateModalView.as_view(), name='technology_add_modal'),
    path('technology/select-options/', technology_select_options, name='technology_select_options'),

    path('party/add/', PartyCreateModalView.as_view(), name='party_add_modal'),
    path('party/select-options/', PartyCreateModalView.as_view(), name='party_select_options'),

    # Dashboard
    path('dashboard/executive/', DashboardExecutiveView.as_view(), name='dashboard_executive'),
    path('dashboard/client/', ClientDashboardView.as_view(), name='dashboard_client_view'),
    # Dashboard
    # path('', DashboardView.as_view(), name='dashboard'),
]