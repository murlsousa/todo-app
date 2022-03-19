from flask import Flask,request
from flask_restful import Api, Resource, reqparse

from src.task import TaskDAOMock

app = Flask(__name__)

api = Api(app)

taskDAOMock = TaskDAOMock()

class TaskEndpoint(Resource):
    
    # TODO: Look into reqparse?
    # Example:
    # parser = reqparse.RequestParser()
    # parser.add_argument('title',
    #     type=str,
    #     required=True,
    #     help = "A task must have at least 3 characters."
    # )
    # USAGE:
    # data = TaskEndpoint.parser.parse_args()
 
    def get(self, id : int):
        tasks = taskDAOMock.retrieve_tasks()
        return {'tasks':list(x.encode_json() for x in tasks)}
 
    def post(self):
        data = request.get_json()
        new_task = taskDAOMock.persist_task(data['title'])
        
        return new_task.encode_json(), 201

api.add_resource(TaskEndpoint, '/api/task')

app.debug = True

if __name__ == '__main__':
    app.run(host='localhost', port=5000)