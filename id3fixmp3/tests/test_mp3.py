#!/usr/bin/env python
# encoding: utf-8
'''
MP3.py

'''

import unittest
import os
import sys
from distutils.dir_util import copy_tree, remove_tree

from id3fixmp3 import MP3

FIXTURES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
FIXTURES_TEST_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures_test')
FILE_WITH_NO_ID3 = '03 - Autumn.mp3'
FILE_WITH_NO_ID3_BAD_NAME = 'vivaldi.mp3'
FILE_WITH_NO_ID3_CUSTOM_NAME = '03 - Autumn - Vivaldi.mp3'

class TestMP3(unittest.TestCase):

    def setUp(self):
        copy_tree(FIXTURES_FOLDER, FIXTURES_TEST_FOLDER)
    
    def tearDown(self):
        remove_tree(FIXTURES_TEST_FOLDER)
    
    def _fixturesFilepath(self, filename):
        return os.path.join(FIXTURES_TEST_FOLDER, filename)
    
    def testLoadFileWithNoID3(self):
        mp3_file = MP3(self._fixturesFilepath(FILE_WITH_NO_ID3))
        self.assertEquals(0, len(mp3_file.getTags()))

    def testGetID3Tag(self):
        mp3_file = MP3(self._fixturesFilepath(FILE_WITH_NO_ID3))
        mp3_file.setFileNameInfo()
        self.assertEquals('Autumn', mp3_file.getTag('title'))
        self.assertEquals(None, mp3_file.getTag('NotExists'))

    def testSetID3Tag(self):
        mp3_file = MP3(self._fixturesFilepath(FILE_WITH_NO_ID3))
        self.assertTrue(mp3_file.setTag('title', 'Autumn'))
        self.assertEquals('Autumn', mp3_file.getTag('title'))
    
    def testSetInvalidID3Tag(self):
        mp3_file = MP3(self._fixturesFilepath(FILE_WITH_NO_ID3))
        self.assertFalse(mp3_file.setTag('unknown_tag', 'Autumn'))
    
    def testSetTrackNumberFromFilename(self):
        mp3_file = MP3(self._fixturesFilepath(FILE_WITH_NO_ID3))
        self.assertEquals(0, len(mp3_file.getTags()))
        mp3_file.setFileNameInfo()
        mp3_file.save()
        self.assertEquals(2, len(mp3_file.getTags()))
        self.assertEquals('03', mp3_file.getTag('tracknumber'))
        self.assertEquals('Autumn', mp3_file.getTag('title'))

    def testUnsuccessfullySetTrackNumberFromFilename(self):
        mp3_file = MP3(self._fixturesFilepath(FILE_WITH_NO_ID3_BAD_NAME))
        self.assertEquals(0, len(mp3_file.getTags()))
        mp3_file.setFileNameInfo()
        mp3_file.save()
        self.assertEquals(0, len(mp3_file.getTags()))
    
    def testRemoveExtraID3Tags(self):
        mp3_file = MP3(self._fixturesFilepath(FILE_WITH_NO_ID3_BAD_NAME))
        mp3_file.setTag('title', 'Autumn')
        mp3_file.setTag('artist', 'Vivaldi')
        mp3_file.setTag('bpm', 'I dont care this tag')
        mp3_file.setTag('media', 'Garbage')
        self.assertEquals(4, len(mp3_file.getTags()))
        mp3_file.removeID3TagsNotIn(('title', 'artist'))
        self.assertEquals(2, len(mp3_file.getTags()))

    def testMatchFilenameExpression(self):
        mp3_file = MP3(self._fixturesFilepath(FILE_WITH_NO_ID3_CUSTOM_NAME))
        expected_tags = {
            'tracknumber': '03',
            'title': 'Autumn',
            'artist': 'Vivaldi',
        }
        received_tags = mp3_file.getFileNameInfo('(?P<tracknumber>\d+) - (?P<title>.*) - (?P<artist>.*).mp3')
        self.assertEquals(expected_tags, received_tags)
    
    def testSetTrackNumberFromCustomFilename(self):
        mp3_file = MP3(self._fixturesFilepath(FILE_WITH_NO_ID3_CUSTOM_NAME))
        self.assertEquals(0, len(mp3_file.getTags()))
        mp3_file.setFileNameInfo('(?P<tracknumber>\d+) - (?P<title>.*) - (?P<artist>.*).mp3')
        mp3_file.save()
        self.assertEquals(3, len(mp3_file.getTags()))
        self.assertEquals('03', mp3_file.getTag('tracknumber'))
        self.assertEquals('Autumn', mp3_file.getTag('title'))
        self.assertEquals('Vivaldi', mp3_file.getTag('artist'))
    
if __name__ == '__main__':
    unittest.main()