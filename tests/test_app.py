import pytest
import json

from app.app import app, taskDAOMock
from src.task import Task

@pytest.fixture
def client_fxt():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

@pytest.fixture
def existing_task_fxt(client_fxt):
    task = Task("Simple task")
    taskDAOMock.persist_task(task)

    return task

def test_get_tasks(client_fxt, existing_task_fxt):
    response = client_fxt.get('/api/task')
    responseData = json.loads(response.data.decode())
    assert response.status_code == 200
    assert responseData
    assert isinstance(responseData['tasks'], list)
    assert next((x for x in responseData['tasks'] if existing_task_fxt.id == x['id']), None)

def test_get_task(client_fxt, existing_task_fxt):
    response = client_fxt.get('/api/task', query_string={ 'id' = existing_task_fxt.id})
    responseData = json.loads(response.data.decode())
    assert response.status_code == 200
    assert responseData
    assert isinstance(responseData['tasks'], list)
    assert next((x for x in responseData['tasks'] if existing_task_fxt.id == x['id']), None)

def test_create_task(client_fxt):
    taskTitle = 'Testing tasks post endpoint'
    response = client_fxt.post(
            '/api/task',
            data=json.dumps(dict(
                title=taskTitle,
            )),
            content_type='application/json',
        )
    responseData = json.loads(response.data.decode())

    assert response.status_code == 201

    task = Task.decode_json(responseData)

    assert task
    assert task.title == taskTitle
    assert task.id > 0
    assert not task.done

def test_create_task_no_title(client_fxt):
    taskTitle = ''
    response = client_fxt.post(
            '/api/task',
            data=json.dumps(dict(
                title=taskTitle,
            )),
            content_type='application/json',
        )
    
    assert response.status_code == 201

