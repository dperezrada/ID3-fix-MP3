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
    
    def testLoadAlbumInfo(self):
        with Stub() as Http:
            from httplib2 import Http
            connection = Http()
            connection.request(any()) >> (
                json.load(open('fixtures/last_fm/vivaldi_headers.json')),
                open('fixtures/last_fm/vivaldi.xml').read()
            )
        
        lastFM = LastFM()
        album_info = lastFM.getAlbumInfo(artist = 'Antonio Vivaldi', album = 'The four seasons')
        self.assertEquals('Antonio Vivaldi', album_info['artist'])
        self.assertEquals('The Four Seasons', album_info['album'])
        self.assertEquals(14, len(album_info['tracks']))
        self.assertEquals(5, len(album_info['images']))
        self.assertEquals(5, len(album_info['tags']))
        self.assertEquals('http://userserve-ak.last.fm/serve/_/44462085/The+Four+Seasons.jpg', album_info['images']['mega'])
        
        
            
if __name__ == '__main__':
    unittest.main()