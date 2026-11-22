from contextlib import contextmanager
import sqlite3
from typing import Generator, Optional

DB_NAME = "tasks.db"


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.commit()


def create_task(title: str, description: Optional[str]) -> dict:
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (title, description, completed) VALUES (?, ?, 0)",
            (title, description),
        )
        conn.commit()
        task_id = cursor.lastrowid
        return get_task_by_id(task_id)  # type: ignore


def get_all_tasks() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
        return [dict(row) for row in rows]


def get_task_by_id(task_id: int) -> Optional[dict]:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        return dict(row) if row else None


def update_task(
    task_id: int,
    title: Optional[str],
    description: Optional[str],
    completed: Optional[bool],
) -> Optional[dict]:
    existing = get_task_by_id(task_id)
    if not existing:
        return None

    new_title = title if title is not None else existing["title"]
    new_description = description if description is not None else existing["description"]
    new_completed = (
        int(completed) if completed is not None else existing["completed"]
    )

    with get_connection() as conn:
        conn.execute(
            """
            UPDATE tasks
            SET title = ?, description = ?, completed = ?
            WHERE id = ?
            """,
            (new_title, new_description, new_completed, task_id),
        )
        conn.commit()

    return get_task_by_id(task_id)


def delete_task(task_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        return cursor.rowcount > 0