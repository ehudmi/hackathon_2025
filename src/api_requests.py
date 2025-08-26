import requests
import json

API_KEY = "af607631e833d6fdd5f27b3bfaa8b2c3"
URL_FIXED = "https://api.themoviedb.org/3/search/"
HEADERS = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhZjYwNzYzMWU4MzNkNmZkZDVmMjdiM2JmYWE4YjJjMyIsIm5iZiI6MTc1NjE0NTY1NS45NDcsInN1YiI6IjY4YWNhN2Y3Y2U2ZDU4OWU5MjlkYjUwZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.pql54nkg8UD7xixVpCvBv-8S880CkFGrkK6cbeN4_Qc",
}


def search_person(name):

    # person_name = "Al Pacino"
    person_query = f"person?query={name}&include_adult=false&language=en-US&page=1"

    url = URL_FIXED + person_query
    response = requests.get(url, headers=HEADERS)
    data = json.loads(response.text)

    # print(data)
    print(data["results"][0]["known_for"][0]["title"])


search_person("Al Pacino")
