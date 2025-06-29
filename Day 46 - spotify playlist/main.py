# GOAL - to create a spotify playlist of top 100 songs on billboard.com on a selected day
import requests
from bs4 import BeautifulSoup
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

spotify_client_id = "342c6e7b5b34479489cae4e34efd088d"
spotify_client_secret = "314a39db3a1a4e509c466d8f48824ad3"
spotify_redirect_uri = "https://example.com/"

def get_top_100_titles(selected_date) -> list:
    """
    Fetches the top 100 titles for a selected date from billboard.com and returns
    :return: list of top 100 titles
    """
    print(f"Getting top 100 titles on {selected_date} from billboard...")

    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
    billboard_url = "https://www.billboard.com/charts/hot-100/" + selected_date.strip()

    response = requests.get(url=billboard_url, headers=header)
    response.raise_for_status()
    website = response.text

    soup = BeautifulSoup(website, "html.parser")

    # list_items = soup.find_all(name="li", class_="o-chart-results-list__item")
    list_items = soup.select("li ul li h3")

    titles = [item.string.strip() for item in list_items]

    # for item in list_items:
    # title_h3 = item.find(name="h3", attrs={"class":"c-title"})
    # if title_h3:
    #     titles.append(title_h3.string.strip())
    return titles


def write_data(selected_date, data: list) -> None:
    """
    Writes the data to a text file
    :param selected_date: user selected date
    :param data: list
    :return: None
    """
    print("Adding the top 100 songs to the file...")

    with open("top_100.txt", "w") as file:
        file.write(f"{selected_date}\n")
        for i in range(len(data)):
            file.write(f"{i + 1}. {data[i]}\n")


def humanize_time(seconds) -> None:
    intervals = [("d", 86400), ("h", 3600), ("m", 60)]
    parts = []
    if seconds:
        for label, count in intervals:
            value, seconds = divmod(seconds, count)

            if value:
                parts.append(f"{value:.0f}{label}")

    parts.append(f"{seconds:.02f}s")
    print(" ".join(parts))


def add_to_playlist(date, titles_to_add):
    print("Authenticating with Spotify...")
    # steps to add the title to the user's spotify playlist
    # 1. get client_id, client_secret from spotify

    # 2. get authorization token from spotify using spotipy
    # spotify authorization
    # playlist-modify-private
    # scope = "user-library-read"
    scope = "playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=spotify_client_id,
                                                   client_secret=spotify_client_secret, redirect_uri=spotify_redirect_uri, show_dialog=True, cache_path="token.txt", username="vgst cof"))
    user_id = sp.current_user()["id"]

    # 3. get an empty playlist id from spotify

    # get the list of playlists in a user profile
    print("Fetching list of playlists...")
    playlist_search_results = sp.current_user_playlists()["items"]

    # check if there are any empty playlists and get its id
    empty_playlist_id = None
    if playlist_search_results:
        print(f"{len(playlist_search_results)} playlists exist")
        # there are playlists in the user profile
        for playlist in playlist_search_results:
            no_of_tracks = int(playlist["tracks"]["total"])
            if not no_of_tracks:
                print(no_of_tracks)
                empty_playlist_id =  playlist["id"]
                empty_playlist_name = playlist["name"]
                print(f"Empty playlist name: {empty_playlist_name}")
                break

    if not playlist_search_results or not empty_playlist_id:
        print("No playlists or no empty playlists exist, creating a new playlist...")
        # if there are no playlists or if there are no empty playlists, create a new playlist
        new_empty_playlist = sp.user_playlist_create(user=user_id, name=f"Top 100 {date}")
        empty_playlist_id = new_empty_playlist["id"]
        empty_playlist_name = new_empty_playlist["name"]
        print(f"New empty playlist name: {empty_playlist_name}")


    # 4. get the id of the title
    print("Adding tracks to the the playlist", end="")
    titles_with_ids = []
    for title in titles_to_add:
        print(".", end="")
        search_results = sp.search(q="track:" + title, type="track")["tracks"]["items"]
        if search_results:
            # if the title exists in spotify db
            title_id = search_results[0]["id"]
            titles_with_ids.append(title_id)
        else:
            print(title, "does not exist in Spotify. Skipped.")

    # 5. add the title to the user's playlist
    sp.playlist_add_items(playlist_id=empty_playlist_id, items=titles_with_ids)


#--------------------#--------------------#

# get the date from the user
user_chosen_date = input("Which year do you want to travel to? Type the date in YYYY-MM-DD: ")

# to track the time for program execution
start_t = time.time()

# get the top 100 songs/titles for the selected date
top_100_titles = get_top_100_titles(user_chosen_date)


if top_100_titles:
    # write the titles to a text file
    write_data(user_chosen_date, top_100_titles)
    # add tracks to the user's playlist
    add_to_playlist(user_chosen_date, top_100_titles)


end_t = time.time()

humanize_time(end_t - start_t)

