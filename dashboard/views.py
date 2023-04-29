from django.shortcuts import render
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

from task_manager.models import CodingTask

import subprocess
import os

from django.shortcuts import render, get_object_or_404

@login_required
def task_list(request):
    coding_tasks = CodingTask.objects.all()
    context = {
        'coding_tasks': coding_tasks
    }

    return render(request, 'dashboard.html', context)

@login_required
def task_completion(request, task_id):
    task = get_object_or_404(CodingTask, id=task_id)

    with open(task.markdown_file.path) as md:
        markdown_text = md.read()

    with open(task.initial_file.path, 'r') as f:
        cs_initial = f.read()

    context = {
        'task': task,
        'markdown_text': markdown_text,
        'code': cs_initial,
    }

    return render(request, 'task.html', context)

@login_required
def run_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        os.chdir('executor')

        f = open('problem.cs', 'w')
        f.write(code)
        f.close()

        subprocess.run(['csc', 'problem.cs'])
    
        if not os.path.isfile('problem.cs'):
            return 'Compilation failed'

        # Execute executable file and capture output
        # output = subprocess.run(['mono', 'problem.exe'])

        return JsonResponse({'output': code})