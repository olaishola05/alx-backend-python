import aiosqlite
import asyncio

async def async_fetch_users():
    async with aiosqlite.connect("user_db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            print("\nAll Users:")
            for row in rows:
                print(row)

async def async_fetch_older_users():
    async with aiosqlite.connect("user_db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            print("\nUsers older than 40:")
            for row in rows:
                print(row)

async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# Run the event loop
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
