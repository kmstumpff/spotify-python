import urllib2
import json

class Query:
    def __init__(self):
        self.metadata = []
        self.json = []
        self.length = 0
        self.num_results = 0
        self.api_url = 'http://ws.spotify.com/search/1/'
        self.media_type = 0
        self.api_media = 'album'
        self.ret_choice = ""

    def check_results(self):
        if self.json:
            return True
        else:
            return False

    def get_title(self, numb):
        if self.media_type == 3:
            return self.json[numb]['name']
        else:
            return "No track available when searching album or artist"

    def get_artist(self, numb):
        if self.media_type == 2:
            return self.json[numb]['name']
        else:
            temp = self.json[numb]['artists']
            return temp[0]['name']

    def get_album(self, numb):
        if self.media_type == 1:
            return self.json[numb]['name']
        elif self.media_type == 2:
            return "No album available when searching artist"
        else:
            temp = self.json[numb]['album']
            return temp['name']

    def get_url(self, numb):
        return self.json[numb]['href']

    def api_call(self, query, s_type):
        #print("query: " + query)
        #print("s_type: " + str(s_type))
        self.media_type = s_type
        if s_type == 1:
            self.api_media = "albums"
            req = self.api_url + "album.json?q=" + query.replace(" ", "+")
            response = json.loads(urllib2.urlopen(req.lower()).read())
            self.metadata = response['info']
            self.json = response['albums']
        if s_type == 2:
            self.api_media = "artists"
            req = self.api_url + "artist.json?q=" + query.replace(" ", "+")
            response = json.loads(urllib2.urlopen(req.lower()).read())
            self.metadata = response['info']
            self.json = response['artists']
        if s_type == 3:
            self.api_media = "tracks"
            req = self.api_url + "track.json?q=" + query.replace(" ", "+")
            response = json.loads(urllib2.urlopen(req.lower()).read())
            self.metadata = response['info']
            self.json = response['tracks']
        else:
            print("Error: API call failed...")
        #print("request: " + req)
        self.length = len(self.json)
        self.num_results = self.metadata['num_results']


class APIError(Exception):
    def __init__(self, value):
        self.message = value

    def __str__(self):
        return repr("There was a problem with your API request: " + self.message)
        
