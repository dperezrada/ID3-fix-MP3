#!/usr/bin/env python
# encoding: utf-8
"""
MP3.py

"""

import re
import os
from mutagen.mp3 import MP3 as MutagenMP3
from mutagen import id3 as MutagenID3
from id3fixmp3 import mutagen_id3_tags

class MP3():
    def __init__(self, filepath):
        self.filepath = filepath
        self.loadID3Info(filepath)

    def setInitialID3(self, filepath):
        mp3_no_id3_file = MutagenMP3(filepath)
        mp3_no_id3_file["TIT2"] = MutagenID3.TIT2(encoding=3, text=[""])    #Setting the title ID3 with nothing, to save it with ID3
        mp3_no_id3_file.save()
    
    def loadID3Info(self, filepath):
        try:    
            self.id3_data = MutagenID3.ID3(filepath)
        except MutagenID3.ID3NoHeaderError:
            self.setInitialID3(filepath)
            self.id3_data = MutagenID3.ID3(filepath)
    
    def _getFileNameInfo(self):
        filename = os.path.basename(self.filepath)
        track_number, song_title = re.match(r'^\s*(\d+)\s*-?\s*(.*)', filename).groups()
        song_title = "".join(song_title.split(".")[:-1]).title()
        return (int(track_number), song_title)

    def getFileNameInfo(self):
        try:
            return self._getFileNameInfo()
        except:
            return (None, None)
    
    def setFileNameInfo(self):
        track_number, song_title = self.getFileNameInfo()
        if track_number:
            self.id3_data.add(MutagenID3.TRCK(encoding=3, text=[track_number]))
        if song_title:
            self.id3_data.add(MutagenID3.TIT2(encoding=3, text=[song_title]))
    
    def getTag(self, key):
        try:
            toReturnTag = self.id3_data[mutagen_id3_tags[key]].text
            return toReturnTag[0]
        except:
            return None

    def setTag(self, key, value):
        try:
            mutagen_key = mutagen_id3_tags[key]
            self.id3_data.add(MutagenID3.__getattribute__(mutagen_key)(encoding=3, text=[value]))
            return True
        except:
            return False
    
    def getTags(self):
        return self.id3_data.keys()
    
    def removeID3TagsNotIn(self, to_mantain_id3_tags):
        mutagen_keys_to_mantain = map(lambda key: mutagen_id3_tags[key], to_mantain_id3_tags)
        actual_id3_elements_to_mantain = {}
        for key, value in self.id3_data.iteritems():
            if key in mutagen_keys_to_mantain:
                actual_id3_elements_to_mantain[key] = value
        self.id3_data.delete()
        for key, value in actual_id3_elements_to_mantain.iteritems():
            self.id3_data.add(value)
    
    def save(self):
        self.id3_data.save()