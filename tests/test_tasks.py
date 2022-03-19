import pytest

from src.task import Task, TaskDAOMock

@pytest.fixture
def task_dao():
    task_dao = TaskDAOMock()

    return task_dao

@pytest.fixture
def existing_task(task_dao):
    task = Task("Simple task")
    task_dao.persist_task(task)

    return task

def test_create_task(task_dao):
    task = Task('Simple task')

    assert task
    assert task.title == 'Simple task'
    assert task.id == None

    persistedTask = task_dao.persist_task(task)

    assert persistedTask.id != None and task.id > 0
    assert persistedTask.title == task.title

def test_retrieve_existing_task(task_dao, existing_task):
    task = task_dao.retrieve_task(existing_task.id)

    assert task
    assert task.id == existing_task.id
    assert task.title == existing_task.title

def test_retrieve_non_existing_task(task_dao):
    task = task_dao.retrieve_task(-1)

def test_retrieve_all_tasks(task_dao):
    task1 = Task("1st task")
    task2 = Task("2nd task")
    task3 = Task("3rd task")
    task1 = task_dao.persist_task(task1)
    task2 = task_dao.persist_task(task2)
    task3 = task_dao.persist_task(task3)
    taskList = task_dao.retrieve_tasks()

    assert len(taskList) >= 3
    assert next((x for x in taskList if task1.id == x.id), None)
    assert next((x for x in taskList if task2.id == x.id), None)
    assert next((x for x in taskList if task3.id == x.id), None)


def test_update_task(task_dao, existing_task):
    oldTitle = existing_task.title
    existing_task.title = 'New title'
    result = task_dao.update_task(existing_task)

    assert result

    updatedTask = task_dao.retrieve_task(existing_task.id)

    assert updatedTask.title == 'New title'

def test_update_non_existing_task(task_dao):
    task = Task('Test')
    task.id = -1

    result = task_dao.update_task(task)

    assert result == False

def test_delete_task(task_dao):
    task = Task('Delete me')
    task_dao.persist_task(task)

    assert task.id

    result = task_dao.delete_task(task.id)

    assert result

    deletedTask = task_dao.retrieve_task(task.id)

    assert deletedTask == None

def test_delete_non_existing_task(task_dao):
    result = task_dao.delete_task(-1)

    assert result == False

def test_do_task(task_dao):

    task = Task('new task')
    
    newTask = task_dao.persist_task(task)

    assert newTask
    assert newTask.done == False

    newTask.done = True

    result = task_dao.update_task(newTask)

    assert result

    task = task_dao.retrieve_task(newTask.id)

    assert task.done

def test_undo_task(task_dao, existing_task):
    existing_task.done = True
    result = task_dao.update_task(existing_task)

    assert result

    existing_task.done = False
    result = task_dao.update_task(existing_task)

    assert result

    task = task_dao.retrieve_task(existing_task.id)

    assert not task.done
