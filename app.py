#importing items needed
from flask import Flask, render_template, request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy

#creating flask app and also using sqlalchemy database to use
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#created general class to be used for each todo
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

#main app page basically will show all todos
@app.route('/')
def index():
    # show all todos
    with app.app_context():
        todo_list = Todo.query.all()
        print(todo_list)
    return render_template('base.html', todo_list=todo_list)


#created functions for each button
#add button
@app.route("/add", methods=["POST"])
def add():
    #add new item
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))
#update button
@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

#delete button
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


#needed to run app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
