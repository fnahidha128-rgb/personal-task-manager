import sqlite3


def get_connection():
    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            due_date TEXT,
            owner_email TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def create_user(email, hashed_password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users(
            email,
            hashed_password
        )
        VALUES (?, ?)
        """,
        (email, hashed_password)
    )

    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    return user 

def create_task(
        title,
        description,
        priority,
        due_date,
        owner_email
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tasks(
            title,
            description,
            priority,
            status,
            due_date,
            owner_email
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            description,
            priority,
            "pending",
            due_date,
            owner_email
        )
    )

    conn.commit()

    task_id = cursor.lastrowid

    conn.close()

    return task_id


def get_all_tasks(owner_email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM tasks
        WHERE owner_email = ?
        """,
        (owner_email,)
    )

    tasks = cursor.fetchall()

    conn.close()

    return tasks


def get_task_by_id(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM tasks
        WHERE id = ?
        """,
        (task_id,)
    )

    task = cursor.fetchone()

    conn.close()

    return task


def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM tasks
        WHERE id = ?
        """,
        (task_id,)
    )

    conn.commit()

    conn.close()
def update_task(
        task_id,
        title,
        description,
        priority,
        status,
        due_date
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET
            title = ?,
            description = ?,
            priority = ?,
            status = ?,
            due_date = ?
        WHERE id = ?
        """,
        (
            title,
            description,
            priority,
            status,
            due_date,
            task_id
        )
    )

    conn.commit()
    conn.close()
def update_task_status(
        task_id,
        status
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET status = ?
        WHERE id = ?
        """,
        (
            status,
            task_id
        )
    )

    conn.commit()
    conn.close()
def get_summary(owner_email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT status, COUNT(*) as count
        FROM tasks
        WHERE owner_email = ?
        GROUP BY status
        """,
        (owner_email,)
    )

    summary = cursor.fetchall()

    conn.close()

    return summary
