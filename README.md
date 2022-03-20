# RadioTO-DO

## Requirements

You should build a simple tasks list so that radiologists don’t forget them.

### Features:

- The user should be able to view (or retrieve) a list of tasks
- Each task should contain a title
- The user should be able to create a task
- The user should be able to edit a task
- The user should be able to mark a task completed
- You need to write only one test, in whatever part of the application suits you better

## Discussion

A simple application to organize one's tasks a bit better. The proposed only have two major entites in it:

* An user;
    * A user has 0 to N tasks
* A task;
    * Has a title
    * Has a state (completed or not)

This is the bare-minimum I believe this application should have:

- CRUD actions related to a task
- REST API
- Unit tests

Some stretch goals if I finish that part and still have more time:

- Add an user abstraction
- Add an ORM
- Run in GCP

## How to install

* Download Poetry (https://github.com/python-poetry/poetry) to develop this small app.
* Download the app from https://github.com/murlsousa/todo-app and clone it.
* Run "poetry install" in the directory of the project.
* You should be ready to start testing

## How to test

Using pytest to run the unit tests.

> poetry run python -m pytest -rP

You can also run the app and use curl (or postman) to access the endpoints:

poetry run python .\app.py

### Get all the tasks

> curl http://localhost:5000/api/task

## Get a single task

Replace #ID# for one of the existing tasks in the system.

> curl http://localhost:5000/api/task/#ID#

### Add a new task

You might need to escape the double quotation marks, or not.

> curl -d '{"title":"A new task"' -H "Content-Type: application/json" -X POST http://localhost:5000/api/task

### To update an existing task

You might need to escape the double quotation marks, or not.

Replace #ID# for one of the existing tasks in the system.

> curl -d '{"title": "testing", "done":"true"}' -H "Content-Type: application/json" -X PUT http://localhost:5000/api/task/#ID#

### To delete an existing task

Replace #ID# for one of the existing tasks in the system.

> curl -H "Content-Type: application/json" -X DELETE http://localhost:5000/api/task/#ID#