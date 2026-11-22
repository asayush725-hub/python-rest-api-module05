# Module 05 (Days 21–25) — Learning Notes: Python REST API Development

## 1. REST Architecture & HTTP Methods
- **RESTful Resource Design:** Structured endpoints around the `/tasks` resource using standard HTTP verbs:
  - `GET /tasks` & `GET /tasks/{task_id}` → Retrieve records (`200 OK`)
  - `POST /tasks` → Create a new task (`201 Created`)
  - `PUT /tasks/{task_id}` → Update an existing task (`200 OK`)
  - `DELETE /tasks/{task_id}` → Delete a task (`204 No Content`)
- **HTTP Error Status Codes:**
  - `401 Unauthorized` when `X-API-Key` is invalid or missing.
  - `404 Not Found` when querying, updating, or deleting a non-existent `task_id`.
  - `422 Unprocessable Entity` when request payloads fail Pydantic validation.

## 2. FastAPI & Interactive Swagger Docs
- Built modular routes in `main.py` using FastAPI path parameters (`task_id: int`), dependency injection (`Depends`), and explicit response models (`response_model=TaskResponse`).
- Leveraged FastAPI's automatic OpenAPI schema generation to test every CRUD endpoint directly in Swagger UI (`/docs`).

## 3. Data Validation with Pydantic (`schemas.py`)
- Separated input and output schemas (`TaskCreate`, `TaskUpdate`, `TaskResponse`) so clients cannot inject read-only fields like `id` or `created_at`.
- Used `Field(..., min_length=1, max_length=120)` to reject empty titles before touching the database.

## 4. SQLite Persistence & SQL Injection Prevention (`database.py`)
- Used Python's built-in `sqlite3` module with `sqlite3.Row` factory to convert query rows cleanly into dictionaries.
- Wrote parameterized SQL queries (`?` placeholders) across all CRUD helpers (`create_task`, `get_tasks`, `get_task`, `update_task`, `delete_task`) to prevent SQL injection.

## 5. Header-Based API Key Authentication (`auth.py`)
- Implemented `APIKeyHeader(name="X-API-Key")` with a reusable `verify_api_key` dependency to protect `/tasks` routes while keeping the `/` health check public.

## 6. Automated Endpoint Testing with Pytest (`test_api.py`)
- Used `pytest` and FastAPI's `TestClient` to test health checks, missing/invalid API keys, Pydantic `422` validation errors, and a full `POST → GET → PUT → DELETE → 404` lifecycle against an isolated temporary SQLite database (`test_tasks.db`).
-