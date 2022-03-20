from flask import Flask,request
from flask_restful import Api, Resource, abort, reqparse

from task import DAOFactory, Task, db

app = Flask(__name__)

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()

taskDAOMock = DAOFactory.get_object_dao('task')

def title_validation():
    def validate(value):
        if len(value) < 3:
            raise ValueError(f"Value must be at least three characters.")
        return value
        
    return validate
    
parser = reqparse.RequestParser()
parser.add_argument('title',
    type=title_validation(),
    required=True,
    help = "A task must have at least 3 characters.",
    trim=True
)

def abort_if_task_not_found(id : int):
    task = taskDAOMock.retrieve(id)
    if not task:
        abort(404, message=f"Task with id {id} doesn't exist.")
    
    return task

class TasksEndpoint(Resource):
    
    def get(self):
        tasks = taskDAOMock.retrieve_all()
        return {'tasks':list(x.encode_json() for x in tasks)}

    def post(self):
        data = request.get_json()
        data = parser.parse_args()

        new_task = Task(data['title'])
        new_task = taskDAOMock.persist(new_task)
        
        return new_task.encode_json(), 201

class TaskEndpoint(Resource):

    def get(self, id : int):
        task = abort_if_task_not_found(id)

        return task.encode_json()
    
    def put(self, id : int):
        data = request.get_json()
        task = abort_if_task_not_found(id)
        task.title = data['title']
        if 'done' in data and data['done'] is not None:
            task.done = True if data['done'] == '1' else False

        taskDAOMock.update(task)
        return task.encode_json(), 200
    
    def delete(self, id : int):
        abort_if_task_not_found(id)
        if taskDAOMock.delete(id):
            return None, 204
        return "¯\\_(ツ)_/¯", 404


api.add_resource(TaskEndpoint, '/api/task/<int:id>')
api.add_resource(TasksEndpoint, '/api/task')

app.debug = True

if __name__ == '__main__':
    app.run(host='localhost', port=5000)