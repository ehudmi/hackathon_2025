from api_requests import get_genres
from db_connection import create_genres

create_genres(get_genres())
