from flask import Flask,request
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)

api = Api(app)

class TasksView(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title',
        type=str,
        required=True,
        help = "A task must have a title."
    )
 
    def get(self):
        # tasks = TaskModel.query.all()
        return {'tasks':list(x.json() for x in [])}
 
    # def post(self):
    #     data = request.get_json()
    #     data = TasksView.parser.parse_args()
 
    #     new_task = TaskModel(data['title'])
    #     db.session.add(new_task)
    #     db.session.commit()
    #     return new_task.json(), 201

api.add_resource(TasksView, '/api/tasks')

app.debug = True

if __name__ == '__main__':
    app.run(host='localhost', port=5000)