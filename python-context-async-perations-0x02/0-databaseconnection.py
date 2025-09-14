import sqlite3

class DatabaseConnection:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        # Open connection
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor  # return cursor so we can run queries directly

    def __exit__(self, exc_type, exc_value, traceback):
        # Commit changes if no errors
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        # Close connection
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

# Example usage:
if __name__ == "__main__":
    # Create sample database and table (for demo purposes)
    with DatabaseConnection("example.db") as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER
            )
        """)
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 25))
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Bob", 30))

    # Use context manager to fetch and print results
    with DatabaseConnection("example.db") as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print("Users in database:")
        for row in results:
            print(row)
