from flask import Flask, request, render_template, url_for, redirect
from my_app.models import ToDo, db, Subtask


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


app = create_app()


@app.get('/')
def home():
    status = request.args.get('status')  # Отримуємо параметр 'status' з URL
    if status == 'active':
        todo_list = ToDo.query.filter_by(is_complete=False).all()
    elif status == 'completed':
        todo_list = ToDo.query.filter_by(is_complete=True).all()
    else:
        todo_list = ToDo.query.all()

    return render_template('my_app/index.html', todo_list=todo_list, title='Головна сторінка')


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        new_todo = ToDo(title=title, is_complete=False)
        db.session.add(new_todo)
        db.session.commit()

        todo_id = new_todo.id

        # Достатньо велике значення, щоб охопити всі можливі поля
        subtask_titles = [request.form.get(f'subtask_title_{i}') for i in range(1, 9999)]
        for subtask_title in subtask_titles:
            if subtask_title:
                new_subtask = Subtask(title=subtask_title, is_complete=False, todo_id=todo_id)
                db.session.add(new_subtask)

        db.session.commit()

    return redirect(url_for('home'))


@app.post('/update/<int:todo_id>')
def update(todo_id):
    todo = ToDo.query.get_or_404(todo_id)

    # Оновлення стану нотатки
    todo.is_complete = not todo.is_complete

    # Оновлення стану підпунктів
    for subtask in todo.subtasks:
        subtask.is_complete = todo.is_complete

    db.session.commit()
    return redirect(url_for('home'))


@app.post('/edit/<int:todo_id>')
def edit(todo_id):
    todo = ToDo.query.get_or_404(todo_id)
    new_title = request.form.get('title')
    todo.title = new_title

    subtasks = []
    for key, value in request.form.items():
        if key.startswith('subtask_title_'):
            subtask_id = int(key.split('_')[-1])
            subtask_title = value
            subtasks.append((subtask_id, subtask_title))

    Subtask.query.filter_by(todo_id=todo_id).delete()

    for subtask_id, subtask_title in subtasks:
        new_subtask = Subtask(title=subtask_title, is_complete=False, todo_id=todo_id)
        db.session.add(new_subtask)

    db.session.commit()
    return redirect(url_for('home'))


@app.get('/delete/<int:todo_id>')
def delete(todo_id):
    todo = ToDo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))


@app.post('/add/subtask/<int:todo_id>')
def add_subtask(todo_id):
    todo = ToDo.query.get_or_404(todo_id)
    title = request.form.get('subtask_title')
    new_subtask = Subtask(title=title, is_complete=False, todo_id=todo.id)
    db.session.add(new_subtask)
    db.session.commit()
    return redirect(url_for('home'))


@app.post('/update/subtask/<int:subtask_id>')
def update_subtask(subtask_id):
    subtask = Subtask.query.get_or_404(subtask_id)

    subtask.is_complete = not subtask.is_complete

    # Оновлення стану нотатки відповідно до стану підпунктів
    todo = subtask.todo
    all_subtasks_complete = all(subtask.is_complete for subtask in todo.subtasks)
    todo.is_complete = all_subtasks_complete

    db.session.commit()
    return redirect(url_for('home'))


@app.post('/delete/subtask/<int:subtask_id>')
def delete_subtask(subtask_id):
    subtask = Subtask.query.get_or_404(subtask_id)
    db.session.delete(subtask)
    db.session.commit()
    return redirect(url_for('home'))


@app.post('/add_subtask/<int:todo_id>')
def add_edit_subtask(todo_id):
    todo = ToDo.query.get_or_404(todo_id)
    subtask_title = request.form.get('subtask_title')
    new_subtask = Subtask(title=subtask_title, is_complete=False, todo_id=todo.id)
    db.session.add(new_subtask)
    db.session.commit()
    return redirect(url_for('home'))
