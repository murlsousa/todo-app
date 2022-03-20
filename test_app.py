from turtle import title
import pytest
import json

from app import app, taskDAOMock
from task import Task, db

@pytest.fixture
def client_fxt():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

@pytest.fixture
def database(request):
    db.app = app
    db.drop_all()
    db.create_all()

    return db

@pytest.fixture
def existing_task_fxt(database):
    task = Task("Simple task")
    database.session.add(task)
    database.session.commit()

    return task

def test_get_tasks(client_fxt, existing_task_fxt):
    response = client_fxt.get('/api/task')
    responseData = json.loads(response.data.decode())
    assert response.status_code == 200
    assert responseData
    assert isinstance(responseData['tasks'], list)
    assert next((x for x in responseData['tasks'] if existing_task_fxt.id == x['id']), None)

def test_get_task(client_fxt, existing_task_fxt):
    response = client_fxt.get(f'/api/task/{existing_task_fxt.id}')
    assert response.status_code == 200
    responseData = json.loads(response.data.decode())
    assert responseData
    task = Task.decode_json(responseData)

    assert task
    assert task.title == existing_task_fxt.title
    assert task.done == existing_task_fxt.done
    assert task.id == existing_task_fxt.id

def test_get_non_existing_task(client_fxt):
    response = client_fxt.get(f'/api/task/0')
    assert response.status_code == 404

def test_create_task(client_fxt):
    taskTitle = 'Testing tasks post endpoint'
    response = client_fxt.post(
            '/api/task',
            data=json.dumps(dict(
                title=taskTitle,
            )),
            content_type='application/json',
        )

    assert response.status_code == 201

    responseData = json.loads(response.data.decode())
    task = Task.decode_json(responseData)

    assert task
    assert task.title == taskTitle
    assert task.id > 0
    assert not task.done

def test_create_task_no_title(client_fxt):
    response = client_fxt.post(
            '/api/task',
            data=json.dumps(dict(
            )),
            content_type='application/json',
        )
    
    assert response.status_code == 400

def test_update_task(client_fxt, existing_task_fxt):
    response = client_fxt.put(
            f'/api/task/{existing_task_fxt.id}',
            data=json.dumps(dict(
                title='update me!',
                done='1'
            )),
            content_type='application/json',
        )
    
    assert response.status_code == 200

    responseData = json.loads(response.data.decode())
    task = Task.decode_json(responseData)
    assert task
    assert task.id == existing_task_fxt.id
    assert task.title == 'update me!'
    assert task.done

def test_delete_task(client_fxt):
    # assume task creation is working since this is tested elsewhere.

    taskTitle = 'Testing tasks post endpoint'
    response = client_fxt.post(
            '/api/task',
            data=json.dumps(dict(
                title=taskTitle,
            )),
            content_type='application/json',
        )

    responseData = json.loads(response.data.decode())
    task = Task.decode_json(responseData)

    assert task
    assert task.id

    responseDelete = client_fxt.delete(f'/api/task/{task.id}')

    assert responseDelete.status_code == 204
