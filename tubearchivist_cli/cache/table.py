import sqlite3


class DatabaseTable:
    def __init__(self, database_path="tubearchive.sqlite"):
        self.database_path = database_path
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()
    
    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def clear_table(self):
        query = f"DELETE FROM {self.database_name}"
        self.execute(query)
        self.commit()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
