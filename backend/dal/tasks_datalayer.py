from Database.connection import DatabaseConnection

class TasksDL:
    def __init__(self):
        self.db = DatabaseConnection().get_connection()

    def pending(self):
        cur = self.db.cursor(dictionary=True)
        cur.execute("SELECT * FROM tasks WHERE status='pending'")
        return cur.fetchall()

    def mark_done(self, tid):
        cur = self.db.cursor()
        cur.execute("UPDATE tasks SET status='done' WHERE id=%s", (tid,))
        self.db.commit()