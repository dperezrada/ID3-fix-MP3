from httplib2 import Http
from config import LASTFM_API_KEY
from urllib import quote_plus
from lxml import etree

class LastFM(object):
    def __init__(self):
        self.connection = Http()
        
    def _makeRequest(self, url):
        headers, body = self.connection.request(url)
        return etree.fromstring(body)
    
    def _runXpathAndAssignToDict(self, tree, xpath, value_name, info_dict):
        xpath_result = tree.xpath(xpath)
        if len(xpath_result) == 1:
            info_dict[value_name] =  xpath_result[0]
        else:
            info_dict[value_name] =  xpath_result
    
    def _processImages(self, images, info_dict):
        info_dict['images'] = {}
        for image in images:
            info_dict['images'][image.get('size')] = image.text
    
    def _processTracks(self, tracks, info_dict):
        info_dict['tracks'] = []
        for track in tracks:
            current_track = {}
            self._runXpathAndAssignToDict(track, './@rank', 'number', current_track)
            self._runXpathAndAssignToDict(track, './name/text()', 'name', current_track)
            self._runXpathAndAssignToDict(track, './/duration/text()', 'duration', current_track)
            self._runXpathAndAssignToDict(track, './/artist/name/text()', 'artist', current_track)
            info_dict['tracks'].append(current_track)
            
    def getAlbumInfo(self, album, artist = None):
        tree = self._makeRequest('http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=%s&artist=%s&album=%s' % (LASTFM_API_KEY, quote_plus(artist), quote_plus(album)))
        albumInfo = {}
        self._runXpathAndAssignToDict(tree, '//album/name/text()', 'album', albumInfo)
        self._runXpathAndAssignToDict(tree, '//album/artist/text()', 'artist', albumInfo)
        self._processImages(tree.xpath('//album/image'), albumInfo)
        self._processTracks(tree.xpath('//tracks/track'), albumInfo)
        self._runXpathAndAssignToDict(tree, '//toptags/tag/name/text()', 'tags', albumInfo)
        return albumInfo
        