# WeGroup Python Examination

This project will test your general Python backend development skills.
We will be using a Python web server framework called [FastAPI](https://fastapi.tiangolo.com/).

## Installation

> First install [pipenv](https://github.com/pypa/pipenv#installation)

To install all required packages run:

```bash
$ pipenv install --dev --skip-lock
```

To run the FastAPI web app

```bash
$ pipenv run server
```

This runs the script 'server' in the Pipfile, it boots up a ASGI web server on port 5000 with custom logging configurations, it also reboots quickly every time you make a file change.
```bash
$ uvicorn app.app:app --reload --log-config logger.conf --log-level debug --port 5000
```

## Exercises

Everything you need to begin is already in place.
In the file [app/api/endpoints/api.py](app/api/endpoints/api.py) you will find some TODO's in comments, they should be sufficient to complete the assignment.

What to do in between:

- Update the `Pipfile` when modifying dependencies.

### General Notes

- Pandas/Numpy are very convenient dependencies, but you should be able to complete the exercises without it.

### EX 1: Index (NET/HTTP)

Retrieve the current Belgian health index for three different base years.

### EX 2: Zipcode (FILE IO)

Retrieve a risk factor ("A", "B" or "C") associated with a Belgian zipcode.

### EX 3: Database

- Setup a Postgres database on your side (docker/local/server) and add the dsn to `.env` (it should be auto read and put to ENV variable).
- Make the previous exercise work without the csv file and by using a database.

### EX 4: Docker

Create a `Dockerfile` to build and run this application, make use of `python:3.8-alpine` as base and make sure to run the app in the docker as non-root. Keep in mind 1 docker container == 1 running process!

Requirements:

- make use of `python:3.8-alpine`
- run as non-root
- 1 running process
- container should be exposed on port 5000
- to install packages just make use of pip, pipenv should not be used in docker (this is because pipenv is an extra dependency that is essentially not required to run your application)

### Ex 5: Caching

- Implement caching, so you don't need to call the database on every request.
- Implement a caching mechanism in the code (memory/redis/memcached/...)
- Where is the best place in the code todo this?
- Implement it.

## Evaluation

If all tests are green, the app works as it should, to run the tests use the pytest command while in your pipenv shell.

```bash
pipenv shell
pytest tests/
```



Things that might be **important**, **read this**:

* If connecting to a database, make sure your tests (unit, e2e, integration) still work, if data is needed in a database, make sure to write a script that does this automatically. If you **write data to database in tests** make sure you 'clean' the database after each test run, so it is possible to test multiple times after each other.
* Git Proficiency
    * Size and quality of commits (message, description and code)
    * Usage of pull requests
    * Logical branching

* Code Refactoring
    * Organising code in a different way can be beneficial

* Testing
    * Writing additional useful tests, or even additional features is a plus!

* Linting and Formatting
    * Using pre-commit to automatically format and lint your code.
