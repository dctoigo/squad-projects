from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.timezone import now
from .models import Task, TimeSession
from ..projects.models import Project
from .forms import TaskForm

from datetime import timedelta
import json
import logging

logger = logging.getLogger(__name__)

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'

    def get_queryset(self):
        return Task.objects.select_related('project', 'responsible')


def task_table(request):
    tasks = Task.objects.select_related('project', 'responsible')
    html = render_to_string('tasks/partials/task_table.html', {'tasks': tasks})
    return HttpResponse(html)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/partials/task_form.html'
    modal_title = "Create Task"
    lookup_field = 'task'

    def get_initial(self):
        initial = super().get_initial()
        project_id = self.request.GET.get("project")
        if project_id:
            try:
                initial["project"] = Project.objects.get(pk=project_id)
            except Project.DoesNotExist:
                pass
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        project = form.initial.get("project") or getattr(form.instance, "project", None)
        if project:
            form.fields["project"].disabled = True
        return form

    def form_valid(self, form):
        form.instance.responsible = self.request.user
        self.object = form.save()

        # Retorna trigger para HTMX atualizar painel
        response = HttpResponse(status=204)
        response["HX-Trigger"] = json.dumps({
            "closeModal": None,
            "taskAdded": {
                "project_id": self.object.project.code
            }
        })
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = self.modal_title
        return ctx


class TaskCreateModalView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/modals/task_add_form.html'
    modal_title = 'Add Task'

    def get_initial(self):
        initial = super().get_initial()
        project_id = self.request.GET.get("project")
        if project_id:
            try:
                initial['project'] = Project.objects.get(pk=project_id)
            except Project.DoesNotExist:
                pass
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.modal_title
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        project = form.initial.get("project") or getattr(form.instance, "project", None)
        if project:
            form.fields['project'].disabled = True
        return form

    def form_valid(self, form):
        form.instance.responsible = self.request.user
        new = form.save()
        row_html = render_to_string("tasks/partials/task_row.html", {"task": new}, request=self.request)

        response = HttpResponse(row_html, status=204)
        response['HX-Trigger'] = json.dumps({
            "closeModal": None,
            "taskAdded": {"project_id": new.project.code if new.project else None}
        })
        return response

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class TaskAddModalView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/modals/task_add_modal.html'

    def get_initial(self):
        initial = super().get_initial()
        project_id = self.request.GET.get('project')
        if project_id:
            initial['project'] = project_id
        return initial

    def form_valid(self, form):
        # Define o usuário responsável
        form.instance.responsible = self.request.user
        self.object = form.save()

        # Retorna resposta HTMX com triggers
        response = HttpResponse(status=204)
        response['HX-Trigger'] = json.dumps({
            'taskAdded': True, # {'project_id': self.object.project.code},
            'closeModal': True,
        })
        return response

    def form_invalid(self, form):
        # Re-renderiza o form com erros
        html = render_to_string(self.template_name, {
            'form': form
        }, request=self.request)
        return HttpResponse(html)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/modals/task_edit_modal.html'
    modal_title = 'Edit Task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.modal_title
        logger.debug('TaskUpdateView.get_context_data called')
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['project'].disabled = True
        return form

    def form_valid(self, form):
        task = form.save()
        
        response = HttpResponse(status=204)
        response['HX-Trigger'] = json.dumps({
            'taskUpdated': True, #{'project_id': task.project.code},
            'closeModal': True,
            'showMessage': {
                'message': 'Task atualizada com sucesso',
                'type': 'success'
            }
        })
        return response

    def form_invalid(self, form):
        # Re-render form with errors
        html = render_to_string(self.template_name, {
            'form': form,
            'title': self.modal_title,
        }, request=self.request)
        return HttpResponse(html)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.time_sessions.exists():
            return HttpResponseForbidden("Can't delete a task with sessions")
        self.object.delete()
        return HttpResponse(status=204)


def task_table_card(request, code):
    project = get_object_or_404(Project, code=code)
    
    # Add debug logging
    active_tasks = project.exclude_closed
    logger.debug(f"Active tasks count: {active_tasks.count()}")
    
    closed_tasks = project.closed
    logger.debug(f"Closed tasks count: {closed_tasks.count()}")
    
    context = {
        "project": project,
        "active_tasks": active_tasks,
        "closed_tasks": closed_tasks,
        "closed_count": closed_tasks.count(),
        "total_closed_duration": project.calculate_closed_duration(),
    }

    html = render_to_string("tasks/partials/task_table_card.html", 
                          context, 
                          request=request)
    return HttpResponse(html)


@require_POST
def toggle_task_session(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if task.responsible != request.user:
        return JsonResponse({
            'error': 'You are not allowed to manage this task.',
            'title': 'Permissão Negada'
        }, status=403)

    session = task.active_session

    if session:
        # Stopping session
        session.stopped_at = now()
        session.save()
        task.status = 'todo'
        task.save()
    else:
        # Check for other active sessions
        active_task = Task.get_active_session_for_user(request.user)
        if active_task:
            return JsonResponse({
                'error': f'Você já tem uma sessão ativa na task "{active_task.description}"',
                'title': 'Sessão em Andamento'
            }, status=400)

        # Create new session
        TimeSession.objects.create(
            task=task,
            user=request.user,
            started_at=now()
        )
        task.status = 'in_progress'
        task.save()

    # Reload complete panel
    project = task.project
    context = {
        "project": project,
        "active_tasks": project.exclude_closed,
        "closed_tasks": project.closed,
        "closed_count": project.closed.count(),
        "total_closed_duration": project.calculate_closed_duration(),
    }
    
    html = render_to_string("tasks/partials/task_table_card.html", 
                          context, 
                          request=request)

    # Retorna apenas o HTML renderizado no campo 'html'    
    return HttpResponse(html)


# def render_task_row(task, request=None):
#     return render_to_string('tasks/partials/task_row.html', {'task': task}, request=request)

@require_POST
def close_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    if task.responsible != request.user:
        return JsonResponse({
            'error': 'You are not allowed to close this task.'
        }, status=403)

    try:
        result = task.close_task()
        
        # Após fechar a task, recarregar o painel completo
        project = task.project
        context = {
            "project": project,
            "active_tasks": project.tasks.exclude(status='closed'),
            "closed_tasks": project.tasks.filter(status='closed'),
            "closed_count": project.tasks.filter(status='closed').count(),
        }
        
        html = render_to_string("tasks/partials/task_table_card.html", 
                              context, 
                              request=request)
        

        return HttpResponse(html)
        # return JsonResponse({
        #     'html': html,
        #     'success': True,
        #     'message': 'Task closed successfully'
        # })
        
    except ValueError as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)