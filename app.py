from flask import Flask, render_template, request, abort, redirect, url_for
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
    return render_template('index.html', tasks=tasks)

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
    # Remove all existing annotations by creating a copy of the list to iterate over
    if hasattr(task, 'annotations') and task.annotations:
        for ann in list(task.annotations):
            task.remove_annotation(ann)

    # Add new annotations from the form
    notes_str = request.form.get('notes', '')
    if notes_str:
        for line in notes_str.splitlines():
            if line.strip():
                task.add_annotation(line.strip())

    task.save()
    
    # The form submission is an HTMX request expecting the full page content
    tasks = w.tasks.pending().filter('+PENDING')
    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True, port=8008)
