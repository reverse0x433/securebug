import sqlite3
DB_NAME = "securebug.db"

ROLES = {"reporter" , "developer" , "admin"}
SEVERITIES = {"low", "medium", "high", "critical"}
STATUSES = {"open", "in_progress", "fixed", "closed"}


def create_user(username, role):
    if role not in ROLES:
        raise ValueError("Invalid Role")
    conn = get_connection()
    curr = conn.cursor()
    curr.execute(
        "INSERT INTO users(username, role) VALUES (?, ?)",
        (username, role)
    )
    conn.commit()
    conn.close()


def create_bug(title, description, severity, reporter_id):
    if severity not in SEVERITIES:
        raise ValueError("Invalid severity")
    conn = get_connection()
    curr = conn.cursor()
    curr.execute(
        "SELECT id, role FROM users WHERE id = ?",
        (reporter_id,)
    )
    reporter = curr.fetchone()
    if reporter is None:
        conn.close()
        raise ValueError("Reporter does not exist")

    reporter_role = reporter["role"]

    if reporter_role not in ROLES:
        conn.close()
        raise ValueError("Invalid reporter role")
    curr.execute(
        """
        INSERT INTO bugs (
            title,
            description,
            severity,
            status,
            reporter_id,
            assignee_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (title, description, severity, "open", reporter_id, None)
    )
    bug_id = curr.lastrowid
    curr.execute(
            """
            INSERT INTO audit_logs (
                actor_id,
                action,
                target_type,
                target_id,
                old_value,
                new_value
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (reporter_id, "create_bug", "bug", bug_id, "none", "open")
        )

    conn.commit()
    conn.close()


def assign_bug(bug_id, assignee_id, actor_id):
    conn = get_connection()
    curr = conn.cursor()
    curr.execute(
        "SELECT id, status, assignee_id FROM bugs WHERE id = ?",
        (bug_id,)
    )
    bug = curr.fetchone()
    if bug is None:
        conn.close()
        raise ValueError("Bug does not exist")
    old_assignee = bug["assignee_id"]
    bug_status = bug["status"]

    if bug_status in ["closed", "fixed"]:
        conn.close()
        raise ValueError("Bug can't be assigned")

    curr.execute(
        "SELECT id, role FROM users WHERE id = ?",
        (actor_id,)
    )
    actor = curr.fetchone()
    if actor is None:
        conn.close()
        raise ValueError("Actor does not exist")

    actor_role = actor["role"]

    if actor_role not in ["developer", "admin"]:
        conn.close()
        raise ValueError("Actor can't assign")

    curr.execute(
        "SELECT id, role FROM users WHERE id = ?",
        (assignee_id,)
    )
    assignee = curr.fetchone()
    if assignee is None:
        conn.close()
        raise ValueError("Assignee does not exist")

    assignee_role = assignee["role"]

    if assignee["role"] != "developer":
        conn.close()
        raise ValueError("Bug can only be assigned to a developer")

    curr.execute(
        "UPDATE bugs SET assignee_id = ? WHERE id = ?",
        (assignee_id, bug_id)
    )
    curr.execute(
            """
            INSERT INTO audit_logs (
                actor_id,
                action,
                target_type,
                target_id,
                old_value,
                new_value
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (actor_id, "assign_bug", "bug", bug_id, old_assignee if old_assignee is not None else "none", f"assigned_to:{assignee_id}")
        )
    conn.commit()
    conn.close()


def change_bug_status(bug_id, new_status, actor_id):
    if new_status not in STATUSES:
        raise ValueError("Invalid status")

    conn = get_connection()
    curr = conn.cursor()
    curr.execute(
        "SELECT id, status, assignee_id FROM bugs WHERE id = ?",
        (bug_id,)
    )
    bug = curr.fetchone()
    if bug is None:
        conn.close()
        raise ValueError("Bug does not exist")

    curr.execute(
        "SELECT id, role FROM users WHERE id = ?",
        (actor_id,)
    )
    actor = curr.fetchone()
    if actor is None:
        conn.close()
        raise ValueError("Actor does not exist")

    actor_role = actor["role"]

    if actor_role not in ["developer", "admin"]:
        conn.close()
        raise ValueError("Actor can't change status")

    current_status = bug["status"]
    assignee_id = bug["assignee_id"]

    if current_status == "closed":
        conn.close()
        raise ValueError("Closed bugs cannot be modified")
    elif current_status == "open" and new_status == "in_progress" and actor_role in ["developer", "admin"] and assignee_id is not None:
        pass
    elif current_status == "in_progress" and new_status == "fixed" and actor_role == "developer":
        pass
    elif current_status == "fixed" and new_status == "in_progress" and actor_role == "admin":
        pass
    elif current_status == "fixed" and new_status == "closed" and actor_role == "admin":
        pass
    else:
        conn.close()
        raise ValueError("Invalid status transition")

    curr.execute(
        "UPDATE bugs SET status = ? WHERE id = ?",
        (new_status, bug_id)
    )
    curr.execute(
            """
            INSERT INTO audit_logs (
                actor_id,
                action,
                target_type,
                target_id,
                old_value,
                new_value
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (actor_id, "change_status", "bug", bug_id, current_status, new_status)
        )
    conn.commit()
    conn.close()


def audit_log(actor_id, action, target_type, target_id, old_value=None, new_value=None):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO audit_logs (
                actor_id,
                action,
                target_type,
                target_id,
                old_value,
                new_value
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (actor_id, action, target_type, target_id, old_value, new_value)
        )

        conn.commit()
        conn.close()
    except Exception:
        pass



def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
