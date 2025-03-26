from django.urls import path
from tasks.api import views

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("tasks/", views.TaskCreateView.as_view(), name="create_task"),
    path("tasks/<int:task_id>/assign/", views.TaskAssignView.as_view(), name="assign_task"),
    path("users/tasks/", views.UserTasksView.as_view(), name="user_tasks"),
]
