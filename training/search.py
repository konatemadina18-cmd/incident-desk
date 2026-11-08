"""Deliberate SQLi sink for the local synthetic exercise only."""
from django.db import connection

def search_incidents(user_id, query):
    if connection.vendor != "sqlite":
        raise RuntimeError("The insecure exercise requires its isolated SQLite database.")
    with connection.cursor() as cursor:
        # Containment: this lookup cannot modify the fixture database. This does NOT
        # prevent SQL injection or disclosure. SQLite execute permits one statement.
        cursor.execute("PRAGMA query_only")
        previous = cursor.fetchone()[0]
        cursor.execute("PRAGMA query_only = ON")
        try:
            # STUDENT TASK: replace concatenation with an owner-scoped ORM query.
            sql = (
                "SELECT id, title, description FROM incidents_incident "
                f"WHERE created_by_id = {int(user_id)} AND title LIKE '%{query}%' "
                "ORDER BY created_at DESC LIMIT 20"
            )
            cursor.execute(sql)
            return [{"id": row[0], "title": row[1], "description": row[2]} for row in cursor.fetchmany(20)]
        finally:
            cursor.execute(f"PRAGMA query_only = {int(previous)}")
