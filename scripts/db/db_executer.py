import sqlite3


class DbExecuter:
    def __init__(self):
        pass

    def execute_query(self, query: str, params: list):
        try:
            db = sqlite3.connect("tasks.db")
            cursor = db.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            db.commit()
            db.close()
            return results
        except sqlite3.Error as error:
            print(f"Error while executing query: {error}")
            return None
