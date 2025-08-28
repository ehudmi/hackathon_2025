import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


connection = psycopg2.connect(
    user=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    host=os.getenv("PGHOST"),
    database=os.getenv("PGDATABASE"),
    sslmode=os.getenv("PGSSLMODE"),
    channel_binding=os.getenv("PGCHANNELBINDING"),
)

cursor = connection.cursor()


def read_from_db(table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    data = [dict(zip(columns, row)) for row in rows]
    return data


# def update_movie(film_id:str):
#     cursor.execute("UPDATE films SET title = %s, col2 = %s WHERE id = %s", (value1, value2, id_value))
#     connection.commit()


def delete_film(film_id: str):
    cursor.execute(f"DELETE FROM films WHERE film_id={film_id}")
    connection.commit()
    return "Film Deleted Successfully"


def insert_film(
    film_id: str, title, release_date, overview, genre_ids, backdrop_url, poster_url
):
    cursor.execute(
        f"""INSERT INTO films(film_id, title, release_date, short_summary, genre_ids,backdrop_url,poster_url)
                       VALUES ({film_id}, '{title}', '{release_date}', '{overview}', ARRAY{genre_ids},{backdrop_url},{poster_url})
                       ON CONFLICT (film_id) DO NOTHING"""
    )
    connection.commit()
    return "Film Added Successfully"


def insert_person(person_id: str, name, role, photo_url):
    cursor.execute(
        f"""INSERT INTO persons(person_id, name, role, photo_url)
                       VALUES ({person_id}, '{name}', '{role}',{photo_url})
                       ON CONFLICT (person_id) DO NOTHING"""
    )
    connection.commit()
    return "Person Added Successfully"


def create_genres(genres_list):
    for genre in genres_list:
        cursor.execute(
            f"""INSERT INTO genres(genre_id, genre_name)
                        VALUES ({genre['id']}, '{genre['name']}')
                        ON CONFLICT (genre_id) DO NOTHING"""
        )
    connection.commit()
    return "Genres Added Successfully"


# if __name__ == "__main__":
#     try:
#         conn = get_connection()
#         print("Connection successful!")
#         conn.close()
#     except Exception as e:
#         print("Connection failed:", e)
