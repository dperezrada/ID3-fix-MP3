#!/usr/bin/env python
# encoding: utf-8

import unittest
import os
import sys
import json

from id3fixmp3 import LastFM
from ludibrio import *

class TestLastFM(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def _mockLastFMRequest(self, body_path = 'fixtures/last_fm/vivaldi.xml', read_format = 'r'):
        with Stub() as Http:
            from httplib2 import Http
            connection = Http()
            headers_path = os.path.join(os.path.dirname(__file__), 'fixtures/last_fm/vivaldi_headers.json')
            body_path = os.path.join(os.path.dirname(__file__), body_path)
            connection.request(any()) >> (
                json.load(open(headers_path)),
                open(body_path, read_format).read()
            )
    
    def testGetAllAlbumInfoGivenTheArtistAndAlbum(self):
        self._mockLastFMRequest()
        lastFM = LastFM()
        album_info = lastFM.getAlbumInfo(artist = 'Antonio Vivaldi', album = 'The four seasons')
        self.assertEquals('Antonio Vivaldi', album_info['artist'])
        self.assertEquals('The Four Seasons', album_info['album'])
        self.assertEquals(14, len(album_info['tracks']))
        self.assertEquals(5, len(album_info['images']))
        self.assertEquals(5, len(album_info['tags']))
        self.assertEquals('http://userserve-ak.last.fm/serve/_/44462085/The+Four+Seasons.jpg', album_info['images']['mega'])

    def testDownloadImage(self):
        self._mockLastFMRequest()
        lastFM = LastFM()
        album_info = lastFM.getAlbumInfo(artist = 'Antonio Vivaldi', album = 'The four seasons')
        self._mockLastFMRequest('fixtures/last_fm/base_cover_image.jpg', 'rb')
        image_destionation_path = os.path.join(os.path.dirname(__file__), 'fixtures/test_downloaded_image.jpg')
        self.assertFalse(os.path.exists(image_destionation_path))
        lastFM.downloadImage(album_info, 'mega', image_destionation_path)
        self.assertTrue(os.path.exists(image_destionation_path))
        os.remove(image_destionation_path)
        
        
        
if __name__ == '__main__':
    unittest.main()