from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.app_context().push()

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_complete = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        
    allTodo = Todo.query.all() 
    return render_template('index.html', allTodo=allTodo)

@app.route('/api/complete/<int:sno>', methods=['PUT'])
def complete_task(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if not todo:
        return jsonify({'error': 'Task not found.'}), 404
    
    todo.is_complete = True
    db.session.commit()
    return jsonify({'success': 'Task marked as complete.'}), 200

@app.route('/api/incomplete/<int:sno>', methods=['PUT'])
def incomplete_task(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if not todo:
        return jsonify({'error': 'Task not found.'}), 404
    
    todo.is_complete = False
    db.session.commit()
    return jsonify({'success': 'Task marked as incomplete.'}), 200

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
