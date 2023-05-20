from django.shortcuts import render
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

from task_manager.models import CodingTask
from accounts.models import UserProfile

import subprocess
import tempfile

from django.shortcuts import render, get_object_or_404

import logging

logger = logging.getLogger(__name__)

@login_required
def task_list(request):
    coding_tasks = CodingTask.objects.all()
    context = {
        'coding_tasks': coding_tasks
    }

    return render(request, 'dashboard.html', context)

@login_required
def task_completion(request, task_id):
    # Retrieve the UserProfile for the current user
    user_profile = request.user.userprofile

    task = get_object_or_404(CodingTask, id=task_id)

    # Check if the task has been completed by the user
    completed_tasks = user_profile.completed_tasks.all()
    task_completed = task in completed_tasks

    with open(task.markdown_file.path) as md:
        markdown_text = md.read()

    with open(task.initial_file.path, 'r') as f:
        cs_initial = f.read()

    context = {
        'task': task,
        'markdown_text': markdown_text,
        'code': cs_initial,
        'task_completed': task_completed,
    }

    return render(request, 'task.html', context)

@login_required
def test_code(request):
    if request.method == 'POST':
        code = request.POST.get('code', '')
        
        with tempfile.NamedTemporaryFile(suffix='.cs', delete=False) as f:
            f.write(code.encode('utf-8'))

        compile_cmd = ['mcs', '-out:program.exe', f.name]
        try:
            result = subprocess.run(compile_cmd, capture_output=True, timeout=10, text=True)
        except subprocess.TimeoutExpired:
            return JsonResponse({'error': 'Code compilation timed out'})
        except subprocess.SubprocessError:
            return JsonResponse({'error': 'Code compilation failed'})

        if result.returncode != 0:
            return JsonResponse({'error': result.stderr})

        execute_cmd = ['mono', 'program.exe']
        try:
            result = subprocess.run(execute_cmd, capture_output=True, timeout=10, text=True)
        except subprocess.TimeoutExpired:
            return JsonResponse({'error': 'Code execution timed out'})

        output = result.stdout
        return JsonResponse({'output': output})

@login_required
def run_code(request):
    if request.method == 'POST':
        # Get the code and task id from the POST data
        code = request.POST.get('code', '')
        task_id = request.POST.get('task', '')

        # Get the task from the database
        task = CodingTask.objects.get(id=task_id)

        # Read the contents of the test file
        with open(task.test_file.path) as f:
            test_code = f.read()

        # Append the test code to the user's code
        code += '\n' + test_code

        # Write the code to a temporary file
        with tempfile.NamedTemporaryFile(suffix='.cs', delete=False) as f:
            f.write(code.encode('utf-8'))

        # Compile the code using mcs
        compile_cmd = ['mcs', '-out:program.exe', f.name]
        try:
            result = subprocess.run(compile_cmd, capture_output=True, timeout=10, text=True)
        except subprocess.TimeoutExpired:
            return JsonResponse({'error': 'Code compilation timed out'})
        except subprocess.SubprocessError:
            return JsonResponse({'error': 'Code compilation failed'})

        if result.returncode != 0:
            # Compilation failed, return the error message
            return JsonResponse({'error': 'Something went wrong when compiling the script, make sure not to change the initial code.'})

        # Execute the compiled code using mono
        execute_cmd = ['mono', 'program.exe']
        try:
            result = subprocess.run(execute_cmd, capture_output=True, timeout=10, text=True)
        except subprocess.TimeoutExpired:
            return JsonResponse({'error': 'Code execution timed out'})
        except subprocess.SubprocessError:
            return JsonResponse({'error': 'Code execution failed'})

        # Return the result as a JSON response
        output = result.stdout[0]

        # Create user profile if it doesn't exist
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = UserProfile.objects.create(user=request.user)
        
        if output == '1':            
            user_profile = UserProfile.objects.get(user=request.user)
            completed_tasks = user_profile.completed_tasks.all()
            if task not in completed_tasks:
                user_profile.completed_tasks.add(CodingTask.objects.get(id=task_id))
            
            return JsonResponse({'output': "Task Completed!"})
        return JsonResponse({'output': "Try Again!"})
    return JsonResponse({'error': 'Invalid request method'})