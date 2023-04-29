from django.urls import path

from . import views

urlpatterns = [
    path('', views.task_list, name='dashboard'), 
    path('tasks/<int:task_id>/completion/', views.task_completion, name='task_completion'),
    
    # path('run-code/', views.run_code, name='run-code'),
]