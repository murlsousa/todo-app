from flask import Flask,request
from flask_restful import Api, Resource, reqparse

from src.task import TaskDAOMock

app = Flask(__name__)

api = Api(app)

taskDAOMock = TaskDAOMock()

class TasksEndpoint(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title',
        type=str,
        required=True,
        help = "A task must have a title."
    )
 
    def get(self):
        tasks = taskDAOMock.retrieve_tasks()
        return {'tasks':list(x.encode_json() for x in tasks)}
 
    def post(self):
        data = request.get_json()
        data = TasksEndpoint.parser.parse_args()
        new_task = taskDAOMock.persist_task(data['title'])
        
        return new_task.encode_json(), 201

api.add_resource(TasksEndpoint, '/api/tasks')

app.debug = True

if __name__ == '__main__':
    app.run(host='localhost', port=5000)