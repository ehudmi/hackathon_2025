import requests
import json
from config import API_KEY, AUTH_TOKEN

URL_FIXED = "https://api.themoviedb.org/3/search/"
HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {AUTH_TOKEN}",
}


def search_person(name):

    person_query = f"person?query={name}&include_adult=false&language=en-US&page=1"
    url = URL_FIXED + person_query
    response = requests.get(url, headers=HEADERS)
    data = json.loads(response.text)

    #  The API may return more than one person
    persons = []
    for person in data["results"]:
        persons.append(
            {
                "id": person["id"],
                "name": person["name"],
                "role": person["known_for_department"],
                "known_for": [
                    {
                        "id": item["id"],
                        "title": item.get("title") or item.get("name", "Unknown Title"),
                        "overview": item["overview"],
                        "poster_path": item["poster_path"],
                        "media_type": item["media_type"],
                        "genre_ids": item["genre_ids"],
                        "release_date": item.get("release_date")
                        or item.get("air_date", "Unknown date"),
                    }
                    for item in person["known_for"]
                ],
            }
        )

    return print(persons)


search_person("robert downey")


def search_movie(movie):

    movie_query = f"movie?query={movie}&include_adult=false&language=en-US&page=1"

    url = URL_FIXED + movie_query
    response = requests.get(url, headers=HEADERS)
    data2 = json.loads(response.text)
    # print(data2)
    print(
        f'Title: {data2["results"][0]["title"]}, Release Date: {data2["results"][0]["release_date"]}'
    )
    print(data2["results"][0]["poster_path"])


# search_movie('Gladiator')


def search_genre(genre):

    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&with_genres={genre}"
    response = requests.get(url, headers=HEADERS)
    data3 = json.loads(response.text)
    # print(data3)
    print(data3["results"][0]["title"])


search_genre("28")


def full_list(full):

    url = f"https://api.themoviedb.org/3/person/{full}/movie_credits?language=en-US"
    response = requests.get(url, headers=HEADERS)
    data4 = json.loads(response.text)

    # To print only the first movie
    # print(data4["cast"][0]["title"])

    # To print the first 5 movies
    dictionary = data4["cast"]
    three_movies = dictionary[:8]
    for item in three_movies:
        print(item["title"])


# full_list(938)
