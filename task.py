import copy
from multipledispatch import dispatch
from flask_sqlalchemy import SQLAlchemy
from abc import ABC, abstractmethod

db = SQLAlchemy()

class Task(db.Model):
    
    __tablename__ = 'tb_tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    done = db.Column(db.Boolean)
    
    def __init__(self, title : str) -> None:
        self.title = title
        self.id = None
        self.done = False

    # TODO turn this into static
    def encode_json(self):
        return { 'id': self.id, 'title': self.title, 'done': 1 if self.done else 0 }

    @staticmethod
    def decode_json(jsonTask : dict):
        task = Task(jsonTask['title'])
        task.id = jsonTask['id']
        task.done = True if jsonTask['done'] else False

        return task
        

class DAOInterface(ABC):

    @abstractmethod
    def persist(self, obj : db.Model) -> db.Model:
        pass

    @abstractmethod
    def retrieve_all(self) -> list[db.Model]:
        pass

    @abstractmethod
    def retrieve(self, id : int) -> db.Model:
        pass

    @abstractmethod
    def update(self, existingObj : db.Model) -> None:
        pass
    
    @abstractmethod
    def delete(self, id : int) -> bool:
        pass


class TaskDAOMock(DAOInterface):

    def __init__(self) -> None:
        self.taskList = []
        self.counter = 0
    
    def persist(self, task : Task) -> Task:
        self.counter += 1
        task.id = self.counter
        persistedTask = copy.deepcopy(task)
        self.taskList.append(persistedTask)

        return persistedTask

    def retrieve_all(self) -> list[Task]:
        return self.taskList

    def retrieve(self, id : int) -> Task:
        return next((x for x in self.taskList if x.id == id), None)
    
    def update(self, existingTask : Task) -> None:
        task = self.retrieve(existingTask.id)

        if task:
            task.title = existingTask.title
            task.done = existingTask.done
            return True
        
        return False
    
    def delete(self, id : int) -> bool:
        existingTask = self.retrieve(id)

        if existingTask:
            self.taskList.remove(existingTask)
            return True
        
        return False

class TaskDBImpl(TaskDAOMock):
    
    def persist(self, task : Task) -> Task:
        newTask = Task(task.title)
        db.session.add(newTask)
        db.session.commit()

        return newTask

    def retrieve_all(self) -> list[Task]:
        return Task.query.all()

    def retrieve(self, id : int) -> Task:
        return Task.query.filter_by(id = id).first()
    
    def update(self, existingTask : Task) -> None:
        task = self.retrieve(existingTask.id)

        if task:
            task.title = existingTask.title
            task.done = existingTask.done
            db.session.add(task)
            db.session.commit()

            return True
        
        return False
    
    def delete(self, id : int) -> bool:
        task = self.retrieve(id)

        if task:
            db.session.delete(task)
            db.session.commit()
            return True
        
        return False

class DAOFactory:

    @staticmethod
    def get_object_dao(type : str) -> DAOInterface:
        if type == 'task':
            return TaskDBImpl()
        
        return None