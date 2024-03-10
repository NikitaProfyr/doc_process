import asyncpg
from os import getenv


from dotenv import load_dotenv
from psycopg2.extensions import cursor

load_dotenv()


async def get_db() -> asyncpg.Connection:
    try:
        conn = await asyncpg.connect(
            database=getenv("DBNAME"),
            user=getenv("USER"),
            password=getenv("PASSWORD"),
            host=getenv("HOST"),
        )
        return conn
    except asyncpg.PostgresError as err:
        print(err)
