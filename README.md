# CULINARY BACKEND

This repository is part of the [culinary app](https://github.com/sergio-prgm/culinary).
It's a backend API built using the [FastAPI](https://tastapi.tiangolo.com) framework.
It handles CRUD operations and supports the OAuth2 password flow for authentication/authorization.

To run it locally, install the dependencies with [Pipenv](https://pypi.org/project/pipenv), activate the `Pipenv` shell and start the server (add the flag `--reload` to update the server when a file changes):

```shell
pipenv install
pipenv shell
uvicorn main:app --reload
```
