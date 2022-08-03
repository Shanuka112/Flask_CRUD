#from crypt import methods
from email.policy import default
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

from sqlalchemy import false

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)

class TodoList(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    #dob = db.Column(db.DateTime, default=datetime.utcnow)
    dob = db.Column(db.String(200), nullable=False)
    amount_due = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return self.student_id

class TodoListSchema(ma.Schema):
    class Meta:
        fields = ('student_id','first_name','last_name','dob','amount_due')

todolist_schema = TodoListSchema(many=False)
todolists_schema = TodoListSchema(many=True)

#Submitting Records
@app.route("/todolist", methods = ["POST"])
def add_todo():
    try:
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        dob = request.json['dob']
        amount_due = request.json['amount_due']
        new_todo = TodoList (first_name = first_name, last_name = last_name, dob=dob, amount_due = amount_due)
        db.session.add(new_todo)
        db.session.commit()
        return todolist_schema.jsonify(new_todo)

    except Exception as e:
        return jsonify({"Error" :"Invalid request."})


#Retriving Records 
@app.route("/todolist", methods = ["GET"])
def get_todos():
    todos = TodoList.query.all()
    result_set = todolists_schema.dump(todos)
    return jsonify(result_set)
    
#Retriving Records by ID
@app.route("/todolist/<int:id>", methods = ["GET"])
def get_todo(id):
    todo = TodoList.query.get_or_404(int(id))
    return todolist_schema.jsonify(todo)


#Updating Records
@app.route("/todolist/<int:id>", methods = ["PUT"])
def update_todo(id):
    todo = TodoList.query.get_or_404(int(id))
    
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    dob = request.json['dob']
    amount_due = request.json['amount_due']

    todo.first_name = first_name
    todo.last_name = last_name
    todo.dob = dob
    todo.amount_due = amount_due

    db.session.commit()
    return todolist_schema.jsonify(todo)


#Deleting a Record
@app.route("/todolist/<int:id>", methods = ["DELETE"])
def delete_todo(id):
    todo = TodoList.query.get_or_404(int(id))
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"Sucess" : "Deleted."})


if __name__ == "__main__": 
    app.run(debug=True)
