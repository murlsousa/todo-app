import pytest

from src.task import Task, TaskDAOMock

@pytest.fixture
def taskDH():
    taskDH = TaskDAOMock()

    return taskDH

@pytest.fixture
def existingTask(taskDH):
    task = Task("Simple task")
    taskDH.persist_task(task)

    return task

def test_create_task(taskDH):
    task = Task('Simple task')

    assert task
    assert task.title == 'Simple task'
    assert task.id == None

    persistedTask = taskDH.persist_task(task)

    assert persistedTask.id != None and task.id > 0
    assert persistedTask.title == task.title

def test_retrieve_existing_task(taskDH, existingTask):
    task = taskDH.retrieve_task(existingTask.id)

    assert task
    assert task.id == existingTask.id
    assert task.title == existingTask.title

def test_retrieve_non_existing_task(taskDH):
    task = taskDH.retrieve_task(-1)

def test_retrieve_all_tasks(taskDH):
    task1 = Task("1st task")
    task2 = Task("2nd task")
    task3 = Task("3rd task")
    task1 = taskDH.persist_task(task1)
    task2 = taskDH.persist_task(task2)
    task3 = taskDH.persist_task(task3)
    taskList = taskDH.retrieve_tasks()

    assert len(taskList) >= 3
    assert next((x for x in taskList if task1.id == x.id), None)
    assert next((x for x in taskList if task2.id == x.id), None)
    assert next((x for x in taskList if task3.id == x.id), None)


def test_update_task(taskDH, existingTask):
    oldTitle = existingTask.title
    existingTask.title = 'New title'
    result = taskDH.update_task(existingTask)

    assert result

    updatedTask = taskDH.retrieve_task(existingTask.id)

    assert updatedTask.title == 'New title'

def test_update_non_existing_task(taskDH):
    task = Task('Test')
    task.id = -1

    result = taskDH.update_task(task)

    assert result == False

def test_delete_task(taskDH):
    task = Task('Delete me')
    taskDH.persist_task(task)

    assert task.id

    result = taskDH.delete_task(task.id)

    assert result

    deletedTask = taskDH.retrieve_task(task.id)

    assert deletedTask == None

def test_delete_non_existing_task(taskDH):
    result = taskDH.delete_task(-1)

    assert result == False

def test_do_task(taskDH):

    task = Task('new task')
    
    newTask = taskDH.persist_task(task)

    assert newTask
    assert newTask.done == False

    newTask.done = True

    result = taskDH.update_task(newTask)

    assert result

    task = taskDH.retrieve_task(newTask.id)

    assert task.done

def test_undo_task(taskDH, existingTask):
    existingTask.done = True
    result = taskDH.update_task(existingTask)

    assert result

    existingTask.done = False
    result = taskDH.update_task(existingTask)

    assert result

    task = taskDH.retrieve_task(existingTask.id)

    assert not task.done
