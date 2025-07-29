from flask import Flask, render_template, request, abort, redirect, url_for, make_response
from tasklib import TaskWarrior, Task
from datetime import datetime

app = Flask(__name__)
w = TaskWarrior()

# Custom filter to format datetime for input fields
@app.template_filter('format_datetime')
def format_datetime(value):
    if not value:
        return ""
    # Format to YYYY-MM-DDTHH:MM for datetime-local input
    return value.strftime('%Y-%m-%dT%H:%M')

def get_task(uuid):
    task = w.tasks.get(uuid=uuid)
    if not task:
        abort(404)
    return task

@app.route('/')
def index():
    tasks = w.tasks.pending().filter('+PENDING')
    projects = sorted(list(set(t['project'] for t in w.tasks.filter(project__not=''))))

    # Filtering logic
    project_filter = request.args.get('project')
    if project_filter:
        if project_filter == 'none':
            tasks = tasks.filter(project__None=True)
        else:
            tasks = tasks.filter(project=project_filter)

    other_filter = request.args.get('filter')
    if other_filter == 'due_today':
        tasks = tasks.filter(due__today=True)

    if request.headers.get('HX-Request'):
        return render_template('_task_list.html', tasks=tasks)

    return render_template('index.html', tasks=tasks, projects=projects)

@app.route('/tasks', methods=['POST'])
def add_task():
    description = request.form.get('description')
    if not description:
        return "", 400
    new_task = Task(w, description=description)
    new_task.save()
    return render_template('_task_item.html', task=new_task)

@app.route('/tasks/<uuid>/toggle', methods=['POST'])
def toggle_task(uuid):
    task = get_task(uuid)
    if task['status'] == 'pending':
        task.done()
    else:
        task.pending()
    task.save()
    return render_template('_task_item.html', task=task)

@app.route('/tasks/<uuid>', methods=['DELETE'])
def delete_task(uuid):
    task = get_task(uuid)
    task.delete()
    return "", 200

@app.route('/edit/<uuid>', methods=['GET'])
def edit_task_page(uuid):
    task = get_task(uuid)
    return render_template('edit_task.html', task=task)

@app.route('/update/<uuid>', methods=['POST'])
def update_task(uuid):
    task = get_task(uuid)
    
    task['description'] = request.form.get('description', task['description'])
    
    project = request.form.get('project')
    task['project'] = project if project else None

    due_str = request.form.get('due')
    if due_str:
        task['due'] = datetime.strptime(due_str, '%Y-%m-%dT%H:%M')
    else:
        task['due'] = None

    scheduled_str = request.form.get('scheduled')
    if scheduled_str:
        task['scheduled'] = datetime.strptime(scheduled_str, '%Y-%m-%dT%H:%M')
    else:
        task['scheduled'] = None

    # --- Correctly handle tags ---
    tags_str = request.form.get('tags', '')
    if tags_str:
        task['tags'] = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
    else:
        task['tags'] = []

    # --- Correctly handle annotations (notes) ---
    if hasattr(task, 'denotate'):
        task.denotate()

    # Add new annotations from the form
    notes_str = request.form.get('notes', '')
    if notes_str:
        for line in notes_str.splitlines():
            if line.strip():
                task.add_annotation(line.strip())

    task.save()
    
    referer = request.form.get('referer', url_for('index'))
    if request.headers.get('HX-Request'):
        response = make_response('', 204)
        response.headers['HX-Redirect'] = referer
        return response
    return redirect(referer)

if __name__ == '__main__':
    app.run(debug=True, port=8008)
