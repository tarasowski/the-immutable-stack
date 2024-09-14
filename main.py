from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

# Sample tasks with a global counter
tasks = [{"id": 1, "task": "Buy groceries"}, {"id": 2, "task": "Do laundry"}]
task_id_counter = 3
counter_value = 10


@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)


@app.route('/hybrid')
def hybrid():
    return render_template('hybrid.html', counter_value=counter_value)


@app.route('/client')
def client():
    return render_template('client.html', counter_value=counter_value)


@app.route('/add', methods=['POST'])
def add_task():
    global task_id_counter
    task = request.form['task']
    if task:
        task_id = task_id_counter
        tasks.append({'id': task_id, 'task': task})
        task_id_counter += 1
        # Return the new <li> element
        return f'''
            <li id="task-{task_id}">{task}
                <button hx-delete="/delete/{task_id}" hx-target="#task-{task_id}" hx-swap="outerHTML">Remove</button>
            </li>
        '''
    return '', 400


@app.route('/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    # Remove the task with the given id
    tasks = [task for task in tasks if task['id'] != task_id]
    return '', 200  # Return a 200 OK response, HTMX will handle removing the task


@app.route('/increment', methods=['GET'])
def increment_counter():
    global counter_value
    counter_value += 1
    time.sleep(0.3)
    return str(counter_value)


if __name__ == '__main__':
    app.run(debug=True)
