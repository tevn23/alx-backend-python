import sqlite3

class ExecuteQuery:
    def __init__(self, db_name: str, query: str, params: tuple = ()):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        # Open DB connection
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        # Execute query
        self.cursor.execute(self.query, self.params)
        # Store results
        self.results = self.cursor.fetchall()
        return self.results  # returned to the "with" block

    def __exit__(self, exc_type, exc_value, traceback):
        # Rollback on error
        if exc_type:
            self.connection.rollback()
        else:
            self.connection.commit()
        # Close resources
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


# Example usage
if __name__ == "__main__":
    db_name = "example.db"

    # Setup database with sample data
    with sqlite3.connect(db_name) as conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS users")
        cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        cur.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [
            ("Alice", 22),
            ("Bob", 27),
            ("Charlie", 30),
            ("Diana", 24),
        ])
        conn.commit()

    # Use our custom context manager to fetch users older than 25
    query = "SELECT * FROM users WHERE age > ?"
    with ExecuteQuery(db_name, query, (25,)) as results:
        print("Users older than 25:")
        for row in results:
            print(row)
