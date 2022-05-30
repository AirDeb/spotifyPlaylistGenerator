import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import json
import re 
import random

def backend(userName, clientSecret, finalGenre, numberOfSongs, playlistName, playlistDescription, playlistPrivacy):
    def remove_duplicates(list):
        no_duplicates = []
        for element in list:
            if element not in no_duplicates:
                no_duplicates.append(element)
        return no_duplicates

    scope= 'ugc-image-upload user-library-modify user-library-read user-read-email user-read-private streaming app-remote-control playlist-read-collaborative playlist-modify-public playlist-read-private playlist-modify-private user-top-read user-read-playback-position user-read-recently-played user-follow-read user-follow-modify ugc-image-upload user-modify-playback-state user-read-playback-state user-read-currently-playing'
    username = userName
    cid= 'a8368076e4e542b590da55e0b96acb29'
    secret = clientSecret
    redirect = 'http://127.0.0.1:8080/'

    token = SpotifyOAuth(username=username, scope=scope, client_id=cid, client_secret=secret, redirect_uri=redirect)
    spotifyObject = spotipy.Spotify(auth_manager = token, requests_timeout=30, retries=30)

    #sets the genre
    user_genre = finalGenre

    #sets the number of songs
    number_of_songs = numberOfSongs

    #Asks user for a playlist name and description
    playlist_name = playlistName
    playlist_description = playlistDescription

    #Asks user for a private or public playlist 
    if playlistPrivacy == "public":
        public_value = True
    else:
        public_value = False    

    #Creates the playlist 
    spotifyObject.user_playlist_create(user=username, name=playlist_name, public=public_value, description=playlist_description)

    #scraping the user's top listened to artists that match with the genre

    preferred_artists = []

    top_artists_result= spotifyObject.current_user_top_artists(limit=100000, offset=0)
    #print(json.dumps(top_artists_result, sort_keys=4, indent=4))

    for each in top_artists_result['items']:
        for artist_genre in each['genres']: 
            if(re.search(user_genre, artist_genre)):
                preferred_artists.append(each['id'])
                break 

    #scraping the artists from the user's current playlists that match with the genre 
    #print(json.dumps(top_playlist_result, sort_keys=4, indent=4))
    #print(json.dumps(playlist_items, sort_keys=4, indent=4))
    top_playlist_result = spotifyObject.current_user_playlists(limit=50, offset=0)
    for each in top_playlist_result['items']:
        playlist_id = each['id']
        playlist_items= spotifyObject.playlist_items(playlist_id, fields=None, limit=100, market=None, additional_types=('track', 'episode')) 
        for playlist_artist in playlist_items['items']:
            artist_data = playlist_artist['track']['album']['artists']
            for artist_name in artist_data:
                artist_id = artist_name['id']
                name_of_artist = artist_name['name']
                artist_information = spotifyObject.artist(artist_id)
                for genre_style in artist_information['genres']:
                    if(re.search(user_genre, genre_style)):
                        preferred_artists.append(artist_id)
                        break  

    #scraping the artists from the user's saved albums that match with the genre 
    saved_albums= spotifyObject.current_user_saved_albums(limit=50, offset=0, market=None)
    #print(json.dumps(saved_albums, sort_keys=4, indent=4))
    for each in saved_albums['items']:
        saved_artist_info = each['album']['artists']
        #print(json.dumps(saved_artist_info, sort_keys=4, indent=4))
        artist_info_id = saved_artist_info[0]["id"]
        artist_info = spotifyObject.artist(artist_info_id)
        for genres_for_artists in artist_info['genres']:
            if re.search(user_genre, genres_for_artists):
                preferred_artists.append(artist_info_id)
                break

    #scraping the artists from the user's top tracks that match with the genre
    top_tracks = spotifyObject.current_user_top_tracks(limit = 1000, offset=0)
    #print(json.dumps(top_tracks, sort_keys=4, indent=4))
    for each in top_tracks['items']:
        info_of_artist = each['album']['artists']
        id_of_artist = info_of_artist[0]['id']
        more_artist_info = spotifyObject.artist(id_of_artist)
        for genre_styles in more_artist_info['genres']:
            if re.search(user_genre, genre_styles):
                preferred_artists.append(id_of_artist)
                break

    #scraping the artists from the user's recently played tracks that match with the genre

    recently_played = spotifyObject.current_user_recently_played(limit=50, after=None, before=None)
    #print(json.dumps(recently_played, sort_keys=4, indent=4))
    for each in recently_played['items']:
        recently_played_id= each['track']['artists'][0]['id']
        recently_played_artist_info = spotifyObject.artist(recently_played_id)
        for recent_genre_style in recently_played_artist_info['genres']:
            if re.search(user_genre, recent_genre_style):
                preferred_artists.append(recently_played_id)
                break

    #removes the artist id duplicates in the list       

    artists_no_dup = remove_duplicates(preferred_artists)
    #print(artists_no_dup)

    #finds some similar artists to the ones already scraped
    
    final_artists_no_dup = []

    if number_of_songs >= 50 or len(artists_no_dup) <= 5: 
        for artist in artists_no_dup:
            count = 0 
            related_artists = spotifyObject.artist_related_artists(artist)
            #print(json.dumps(related_artists, sort_keys=4, indent=4))
            for the_artist_info in related_artists['artists']:
                for genres_of_artist in the_artist_info['genres']:
                    if count < 5 and re.search(user_genre, genres_of_artist) and the_artist_info['id'] not in artists_no_dup and the_artist_info['id'] not in final_artists_no_dup:
                        final_artists_no_dup.append(the_artist_info['id'])
                        count+=1
    else: 
        for artist in artists_no_dup:
            count = 0 
            related_artists = spotifyObject.artist_related_artists(artist)
            #print(json.dumps(related_artists, sort_keys=4, indent=4))
            for the_artist_info in related_artists['artists']:
                for genres_of_artist in the_artist_info['genres']:
                    if count < 2 and re.search(user_genre, genres_of_artist) and the_artist_info['id'] not in artists_no_dup and the_artist_info['id'] not in final_artists_no_dup:
                        final_artists_no_dup.append(the_artist_info['id'])
                        count+=1

    for each in artists_no_dup:
        final_artists_no_dup.append(each)
    
    #finding all the songs for each artist in randomly selected albums

    all_songs= []
    all_albums = []
    #artist_albums = spotifyObject.artist_albums('7kZBQcHbD4IKKEJIMnrRWC', album_type=None, country=None, limit=50, offset=0)
    #print(json.dumps(artist_albums, sort_keys=4, indent=4)) 
    for each in final_artists_no_dup:
        artist_albums = spotifyObject.artist_albums(each, album_type=None, country=None, limit=50, offset=0)
        for album in artist_albums['items']:
            all_albums.append(album['uri'])
    #print(json.dumps(album_track, sort_keys=4, indent=4))
    random.shuffle(all_albums)
    randomized_albums = []
    if len(all_albums) > number_of_songs/2:
        for i in range(int(number_of_songs/2)):
            randomized_albums.append(all_albums[i])
    else:
        randomized_albums = all_albums        
    count = 0
    for each in randomized_albums:
        album_track = spotifyObject.album_tracks(each, limit = 50, offset=0, market=None)
        for song in album_track['items']:
            count+=1
            all_songs.append(song['id'])
        if count >= 10000:
            break

    #shuffles the songs and picks the number of songs the user requested
    random.shuffle(all_songs)
    final_song_list = [] 

    if len(all_songs) >= number_of_songs:
        for i in range(number_of_songs):
            final_song_list.append(all_songs[i])
    else:
        final_song_list = all_songs
    
    #Adds songs to playlist 

    prePlaylist = spotifyObject.user_playlists(user=username)
    playlist = prePlaylist["items"][0]['id']
    spotifyObject.user_playlist_add_tracks(user=username,playlist_id=playlist,tracks=final_song_list)



                