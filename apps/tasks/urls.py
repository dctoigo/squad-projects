from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('table/', views.task_table, name='task_table'),
    path('add/', views.TaskCreateModalView.as_view(), name='task_add'),

    path('add-modal/', views.TaskAddModalView.as_view(), name='task_add_modal'),
 
    path('<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_edit'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('task/<int:pk>/close/', views.close_task, name='task_close'),
    path('<int:pk>/toggle-session/', views.toggle_task_session, name='task_toggle_session'),
    path("panel/<str:code>/", views.task_table_card, name="task_table_card"),
]
