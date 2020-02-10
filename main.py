import requests
import spotipy
import sys
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import json
import time
import pandas as pd
from datetime import datetime

def playlist_data(sp):
    my_songs = []
    ids = []
    offset = 0

    #Calls
    my_play = sp.playlist(playlist)
    #Current date and time
    now = datetime.now()
    #timestamp = datetime.timestamp(now)
    my_play['time'] = now.strftime("%d/%m/%Y, %H:%M:%S")
    aux_time = now.strftime("%d-%m-%Y %H-%M-%S")
    #loop for receive all tracks
    while(True):
        my_tracks = sp.playlist_tracks(playlist, fields=None, limit=100, offset=offset, market=None)
        now = datetime.now()
        my_songs += my_tracks['items']
        if my_tracks['next'] is not None:
            offset += 100
        else:
            break
    #loop for getting id's of the songs
    for x in my_songs:
        ids.append(x['track']['id'])
    index = 0
    my_features = []
    my_songs += now.strftime("%d/%m/%Y, %H:%M:%S")
    #getting the features of each song
    while index < len(ids):
        my_features += sp.audio_features(ids[index:index + 50])
        index += 50
    features_list = []

    for features in my_features:
        features_list.append([features['energy'], features['liveness'],
                                features['tempo'], features['speechiness'],
                                features['acousticness'], features['instrumentalness'],
                                features['time_signature'], features['danceability'],
                                features['key'], features['duration_ms'],
                                features['loudness'], features['valence'],
                                features['mode'], features['type'],
                                features['uri']])
                            
    df = pd.DataFrame(features_list, columns=['energy', 'liveness',
                                        'tempo', 'speechiness',
                                        'acousticness', 'instrumentalness',
                                        'time_signature', 'danceability',
                                        'key', 'duration_ms', 'loudness',
                                        'valence', 'mode', 'type', 'uri'])
    df.to_csv('{}-{}.csv'.format(username, "SadSongs"), index=False)
    my_features += now.strftime("%d/%m/%Y, %H:%M:%S")

    with open('Json/features_data_%s.json' % now.strftime("%d-%m-%Y %H-%M-%S"), 'w') as json_file:
        json.dump(my_features, json_file)
    print("Features File saved")

    with open('Json/track_data_%s.json' % now.strftime("%d-%m-%Y %H-%M-%S"), 'w') as json_file:
        json.dump(my_songs, json_file)
    print("Track File saved")

    with open('Json/playlist_data_%s.json' % aux_time, 'w') as json_file:
        json.dump(my_play, json_file)
    print("Playlist File saved")

if __name__ == "__main__":
    #Configuration
    playlist = ''   #Use your playlist id
    scope = 'user-library-read'
    i = 0
    now = datetime.now()

    #Login
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username" % (sys.argv[0],))
        sys.exit()

    #Use Your client ID, ClientSecret and your redirect_uri as your app is configurated
    token = util.prompt_for_user_token(username,scope,client_id='',client_secret='',redirect_uri='http://localhost/')
    sp = spotipy.Spotify(auth=token)

    while(not time.sleep(60)):
        i += 1
        print("Request Nº: {} at {}".format(i, now.strftime("%d/%m/%Y, %H:%M:%S")))
        playlist_data(sp)