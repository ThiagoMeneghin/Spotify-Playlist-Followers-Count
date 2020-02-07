import requests
import spotipy
import sys
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import json
import pandas as pd

#Configuration
playlist = '3q9WmPPnNCqSyfEGXzp28u'
scope = 'user-library-read'
if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()
token = util.prompt_for_user_token(username,scope,client_id='',client_secret='',redirect_uri='http://localhost/')
sp = spotipy.Spotify(auth=token)
my_songs = []
items = []
ids = []
offset = 0

#Calls
my_play = sp.playlist(playlist)
#loop for receive all tracks
while(True):
    my_tracks = sp.playlist_tracks(playlist, fields=None, limit=100, offset=offset, market=None)
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

with open('Json/features_data.json', 'w') as json_file:
    json.dump(my_features, json_file)

with open('Json/track_data.json', 'w') as json_file:
    json.dump(my_songs, json_file)

with open('Json/play_data.json', 'w') as json_file:
    json.dump(my_play, json_file)
