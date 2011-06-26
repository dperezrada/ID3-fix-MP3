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
    
    def _getFileNameInfo(self, id3_tags_to_match, to_check_expression):
        filename = os.path.basename(self.filepath)
        id3_tags_matches = re.match(re.compile(to_check_expression), filename).groups()
        found_tags = {}
        if len(id3_tags_matches) == len(id3_tags_to_match):
            for i in range(0, len(id3_tags_to_match)):
                found_tags[id3_tags_to_match[i]] = id3_tags_matches[i]
        return found_tags
    
    def _prepareFilenameExpression(self, filename_expression):
        tag_parameter_expression = '\{([^\}]*)\}'
        id3_tags_to_match = re.findall(tag_parameter_expression, filename_expression)
        to_check_expression = re.sub(tag_parameter_expression, '(.*)',  filename_expression)
        return (id3_tags_to_match, to_check_expression)

    def getFileNameInfo(self, filename_expression):   #Default name: {tracknumber} [-] {title}
        try:
            id3_tags_to_match, to_check_expression = self._prepareFilenameExpression(filename_expression)
            return self._getFileNameInfo(id3_tags_to_match, to_check_expression)
        except:
            return {}
    
    def setFileNameInfo(self, filename_expression = '{tracknumber} -? {title}.mp3'):
        for key, value in self.getFileNameInfo(filename_expression).iteritems():
            self.setTag(key, value)
    
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