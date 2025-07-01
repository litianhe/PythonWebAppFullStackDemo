# A Python web application Full Stack Demo(FastAPI+SQLModel+Pydantic+Alembic, Next.js+TypeScript)
Python3 web application Demo for comment tree (including comment tree, user authentication, and Swagger API documentation), using Python3+FastAPI+SQLModel+Pydantic+Alembic as backend, and Next.js+TypeScript as frontend.

## Project Overview
A full-stack application featuring:
- Backend API with Python (FastAPI)
- Frontend UI with Next.js
- Comment tree functionality with nested replies
- User authentication system
- Swagger API documentation
- Docker support

## Technology Stack
- **Backend**: Python, FastAPI, SQLModel, Pydantic, Alembic
- **Frontend**: Next.js, TypeScript
- **Package Management**: [uv](https://docs.astral.sh/uv/)
- **Database**: SQLite (development)
- **API Docs**: Swagger UI is available on `http://<ip>:8000/docs`

## Quickstart Guide

### Prerequisites
- Python 3.11+
- Node.js 18+ (optional)
- Docker (optional)

### How to run
Two ways to run the application:
- Run application locally, or
- Run application in Docker

#### Run application locally 
1. **(Once) Install [uv](https://docs.astral.sh/uv/)**

2. **Setup Environment Variables **:
```bash
cp .env.example .env
make db
```

3. **Run Application Locally**:
```bash
make run
```

#### Run application in Docker
1. build the docker image
```bash
make docker
```
2. run the docker container
```bash
sudo docker run -p 8000:8000 comment-app:v0.0.1
```


## Developer's Guide

### Initial the backend
1. install [uv](https://docs.astral.sh/uv/) which will be used to manage this Python backend.
2. run the following commands to initialize the backend (with alembic + fastapi + pydantic + sqlmodel)
```bash
cd backend
uv venv 
source .venv/bin/activate
uv init
uv add alembic fastapi[standard] pydantic-settings sqlmodel python-jose[cryptography] passlib python-multipart
uv add --dev pytest ruff mypy
alembic init alembic

# Add model in backend/app/database/models, then modify alembic/env.py to add model's metadata,
# finally run the following command to create migration
alembic revision --autogenerate -m "init"
alembic upgrade head

# Testing backend
fastapi run app/main.py
```


### Initial the UI
1. run the following commands to initialize the frontend UI(with next.js)
```bash
cd ui
npx create-next-app@latest .
```
2. change the output config by modifying `next.config.js`
3. install the dependencies
```bash
npm install
```
4. run the following commands to build the static UI
```bash
npm run build
```
5. download swagger UI from [swagger-ui](https://github.com/swagger-api/swagger-ui.git) dist folder
6. update backend code to mount the swagger-ui and static UI


### Run the application
1. create `.env` file by copy and modify file `.env.example`
2. change setting in .env such as `ENVIRONMENT` and `DATABASE_URL` 
3. change `SECRET_KEY` in `.env` file to a random long string in production environment for security reason
4. `make run` to start the application based on the environment from `.env` file


### Run the tests
1. `make test` to run the tests


### Code style and linting
1. `make lint` to run the linting and code style check
2. `make format` to format the code
