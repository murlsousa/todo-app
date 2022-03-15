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
- Simple web frontend
- Unit tests

Some stretch goals if I finish that part and still have more time:

- Add an user abstraction
- Add an ORM
- Run in GCP

## How to run

