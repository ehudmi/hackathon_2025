import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


def get_connection():
    conn = psycopg2.connect(
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        host=os.getenv("PGHOST"),
        database=os.getenv("PGDATABASE"),
        sslmode=os.getenv("PGSSLMODE"),
        channel_binding=os.getenv("PGCHANNELBINDING"),
    )
    return conn


# Example usage:
if __name__ == "__main__":
    try:
        conn = get_connection()
        print("Connection successful!")
        conn.close()
    except Exception as e:
        print("Connection failed:", e)
