import requests
import spotipy
import pprint
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup

URL = "https://www.billboard.com/charts/hot-100/"
CLIENT_ID = "YOUR_SPOTIFY_CLIENT_ID"
CLIENT_SECRET = "YOUR_SPOTIFY_CLIENT_SECRET"
REDIRECT_URI = "http://example.com"


scope = "playlist-modify-private"
auth_manager = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=scope, redirect_uri=REDIRECT_URI, show_dialog=True, cache_path=".cache")
sp = spotipy.Spotify(auth_manager=auth_manager)

user_id = sp.current_user()["id"]

date = input("Which year do you want to listen to? Type the date in this format YYYY-MM-DD: ")
year = date.split("-")[0]
month = date.split("-")[1]
day = date.split("-")[2]

response = requests.get(URL + date)
soup = BeautifulSoup(response.text, "html.parser")
song_titles = [song.getText() for song in soup.find_all(name="span", class_="chart-element__information__song")]
song_uris = []

for song in song_titles:
    song_result = sp.search(q=f"track: {song} year: {year}", type="track")
    try:
        uri = song_result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipping")


playlist_name = f"{year}-{month}-{day} Billboard 100"
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print("Done")
