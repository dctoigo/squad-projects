from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'manager'

urlpatterns = [
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

    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
]