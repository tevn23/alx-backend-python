import asyncio
import aiosqlite

DB_NAME = "example.db"

# Create demo table + data
async def setup_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DROP TABLE IF EXISTS users")
        await db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        await db.executemany(
            "INSERT INTO users (name, age) VALUES (?, ?)",
            [
                ("Alice", 22),
                ("Bob", 45),
                ("Charlie", 50),
                ("Diana", 35),
            ],
        )
        await db.commit()

# Async function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows

# Async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            rows = await cursor.fetchall()
            return rows

# Run both queries concurrently
async def fetch_concurrently():
    results_all, results_older = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("All users:")
    for row in results_all:
        print(row)

    print("\nUsers older than 40:")
    for row in results_older:
        print(row)

if __name__ == "__main__":
    asyncio.run(setup_db())         # setup DB first
    asyncio.run(fetch_concurrently())
