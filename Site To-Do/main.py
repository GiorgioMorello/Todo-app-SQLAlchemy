from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, url_for, redirect, request, flash
from datetime import datetime



app = Flask(__name__)
app.config['SECRET_KEY'] = 'da5e9535e2f62ee9b99c6c195385cdd8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database = SQLAlchemy(app)


class ToDo(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String, nullable=False)
    complete = database.Column(database.Boolean, default=False)
    creation_date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)




@app.route("/")
def home():
    todo_list = ToDo.query.order_by(ToDo.id.desc())
    return render_template('home.html', todo_list=todo_list, datetime=datetime)


@app.route('/add', methods=['POST', 'GET'])
def add():
    title = request.form.get('title')
    # Will create the columns of the table
    new_todo = ToDo(title=title, complete=False)
    database.session.add(new_todo)
    database.session.commit()
    flash("ToDo successfully added", "alert-success")
    return redirect(url_for('home'))


@app.route('/update/<todo_id>', methods=['POST', 'GET'])
def update(todo_id):
   todo = ToDo.query.get(todo_id)
   todo.complete = not todo.complete
   database.session.commit()
   return redirect(url_for('home'))

@app.route('/delete/<todo_id>', methods=['POST', 'GET'])
def delete(todo_id):
   todo = ToDo.query.filter_by(id=todo_id).first()
   database.session.delete(todo)
   database.session.commit()
   flash("ToDo successfully deleted", "alert-danger")
   return redirect(url_for('home'))









if __name__ == '__main__':
    database.create_all()
    app.debug = True
    app.run()