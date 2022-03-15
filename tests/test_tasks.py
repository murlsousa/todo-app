import pytest
import copy

@pytest.fixture
def taskDH():
    taskDH = TaskDataHandler()

    yield taskDH

@pytest.fixture
def existingTask(taskDH):
    task = Task("Simple task")
    taskDH.persist_task(task)

    yield task

class Task:
    
    def __init__(self, title : str) -> None:
        self.title = title
        self.id = None
        self.done = False

class TaskDataHandler:

    def __init__(self) -> None:
        self.taskList = []
        self.counter = 0

    def persist_task(self, task : Task) -> Task:
        self.counter += 1
        task.id = self.counter
        persistedTask = copy.deepcopy(task)
        self.taskList.append(persistedTask)

        return persistedTask

    def retrieve_task(self, id : int) -> Task:
        return next((x for x in self.taskList if x.id == id), None)
    
    def update_task(self, existingTask : Task) -> None:
        # find in list and update
        task = self.retrieve_task(existingTask.id)

        if task:
            task.title = existingTask.title
            task.done = existingTask.done
            return True
        
        return False
    
    def delete_task(self, id : int) -> bool:
        existingTask = self.retrieve_task(id)

        if existingTask:
            self.taskList.remove(existingTask)
            return True
        
        return False
            
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

    assert task == None

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
