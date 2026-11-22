# Task Manager REST API (Module 05)

A RESTful Task Manager API built with **FastAPI**, **SQLite**, **Pydantic**, and **Pytest**. This project implements full CRUD functionality, request/response schema validation, header-based API key authentication, interactive Swagger documentation, and automated endpoint tests.

---

## Features

- **CRUD Operations:** Create, read, update, and delete tasks persisted in a local SQLite database (`tasks.db`).
- **Schema Validation:** Strict request and response validation using Pydantic models (`TaskCreate`, `TaskUpdate`, `TaskResponse`).
- **API Key Authentication:** Protected `/tasks` endpoints secured via the `X-API-Key` HTTP header.
- **Interactive API Docs:** Built-in Swagger UI (`/docs`) and OpenAPI specification (`/openapi.json`).
- **Automated Testing:** Isolated endpoint and lifecycle test suite powered by `pytest` and FastAPI's `TestClient`.

---

## Project Structure

```text
python-rest-api-module05/
├── auth.py          # X-API-Key header validation dependency
├── database.py      # SQLite connection and parameterized CRUD queries
├── main.py          # FastAPI app initialization and route handlers
├── schemas.py       # Pydantic request and response models
├── test_api.py      # Pytest automated test suite
├── .gitignore       # Ignores venv, __pycache__, *.db, and .pytest_cache
└── README.md        # Project documentation