"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Todo
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/todos', methods=['GET'])
def hello_world():
    # puedes convertir esa variable en un string json así

    # get all the people
    todos = Todo.query.all()

    # map the results and your list of people  inside of the all_people variable
    all_todos = list(map(lambda x: x.serialize(), todos))
    
    json_text =jsonify(all_todos)

    return json_text

@app.route('/todos', methods=['POST'])
def add_new_todo():
    request_body = request.get_json()
    todo = Todo(label=request_body["label"], done=request_body["done"])
    db.session.add(todo)
    db.session.commit()

    return jsonify({"Respuesta":"Los datos se almacenaron satisfactoriamente"}), 200


@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)
    if todo is None:
        raise APIException('Todo not found', status_code=404)

    db.session.delete(todo)
    db.session.commit()
   
    return jsonify({"Respuesta":"Los datos se eliminaron satisfactoriamente"}), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
