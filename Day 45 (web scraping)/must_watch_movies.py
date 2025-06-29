# GOAL
# to get the list of top 100 must watch movies from empire online
# save the list to a txt file
import requests
from bs4 import BeautifulSoup, PageElement, Tag, NavigableString
import time

website_url = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

def write_to_file(data: str) -> None:
    # check if file exists
    # if it exists, check if it is empty
    data_file = "movies_to_watch.md"

    with open(data_file, "w", encoding="utf-8") as file:
        file.write(data)

def get_movies():
    response = requests.get(website_url)
    response.raise_for_status()

    website_html = response.text

    soup = BeautifulSoup(website_html, "html.parser")
    movie_title_tags = soup.find_all(name="h3", class_="title")
    # movie_title_tags = soup.select(selector=".title")
    # print(movie_title_tags)

    # movies = []
    #
    # for tag in movie_title_tags:
    #     movies.append(tag.string)


    movies = ["- [ ] " + tag.getText() for tag in movie_title_tags]

    # movies.reverse()
    movies = movies[::-1]
    # print(movies)

    write_to_file("\n".join(movies))


start_t = time.time()

get_movies()

end_t = time.time()

def humanize_time(seconds: float) -> None:
    intervals = [("d", 86400), ("h", 3600), ("m", 60)]

    parts = []

    if seconds:
        for label, count in intervals:
            value, seconds = divmod(seconds, count)

            if value:
                parts.append(f"{int(value)}{label}")

        parts.append(f"{round(seconds, 2)}s")

    print("Elapsed:", " ".join(parts))

humanize_time(end_t - start_t)