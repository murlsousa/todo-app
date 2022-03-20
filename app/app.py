from flask import Flask,request
from flask_restful import Api, Resource, abort, reqparse

from src.task import TaskDAOMock

app = Flask(__name__)

api = Api(app)

taskDAOMock = TaskDAOMock()

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
parser.add_argument('done',
    type=bool,
    help = "A task must have at least 3 characters.",
)

def abort_if_task_not_found(id : int):
    task = taskDAOMock.retrieve_task(id)
    if not task:
        abort(404, message=f"Task with id {id} doesn't exist.")
    
    return task

class TasksEndpoint(Resource):
    
    def get(self):
        tasks = taskDAOMock.retrieve_tasks()
        return {'tasks':list(x.encode_json() for x in tasks)}

    def post(self):
        data = request.get_json()
        data = parser.parse_args()

        new_task = taskDAOMock.persist_task(data['title'])
        
        return new_task.encode_json(), 201

class TaskEndpoint(Resource):

    def get(self, id : int):
        task = abort_if_task_not_found(id)

        return task.encode_json()
    
    def put(self, id : int):
        data = parser.parse_args()
        task = abort_if_task_not_found(id)
        task.title = data['title']
        if data['done']:
            task.done = data['done']

        taskDAOMock.update_task(task)
        return task.encode_json(), 200
    
    def delete(self, id : int):
        abort_if_task_not_found(id)
        if taskDAOMock.delete_task(id):
            return None, 204
        return "¯\\_(ツ)_/¯", 404


api.add_resource(TaskEndpoint, '/api/task/<int:id>')
api.add_resource(TasksEndpoint, '/api/task')

app.debug = True

if __name__ == '__main__':
    app.run(host='localhost', port=5000)