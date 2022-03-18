import copy

class Task:
    
    def __init__(self, title : str) -> None:
        self.title = title
        self.id = None
        self.done = False

class TaskDAOMock:

    def __init__(self) -> None:
        self.taskList = []
        self.counter = 0

    def persist_task(self, task : Task) -> Task:
        self.counter += 1
        task.id = self.counter
        persistedTask = copy.deepcopy(task)
        self.taskList.append(persistedTask)

        return persistedTask

    def retrieve_tasks(self) -> list[Task]:
        return self.taskList


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