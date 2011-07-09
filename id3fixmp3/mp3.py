#!/usr/bin/env python
# encoding: utf-8
"""
MP3.py

"""

import re
import os
from mutagen.mp3 import MP3 as MutagenMP3
from mutagen import id3 as MutagenID3
from id3fixmp3 import mutagen_id3_tags, mutagen_id3_tags_reversed
from mimetypes import guess_type

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
    
    def _getFileNameInfo(self, filename_expression, id3_tags_to_match, base_path):
        if not base_path:
            filename = os.path.basename(self.filepath)
        else:
            filename = self.filepath.replace(base_path, "")
            if filename[0] == '/':
                filename = filename[1:]
        id3_tags_matches = re.match(filename_expression, filename)
        found_tags = {}
        for matched_id3_tag in id3_tags_to_match:
            found_tags[matched_id3_tag] = id3_tags_matches.group(matched_id3_tag)
        return found_tags
    
    def _getFilenameExpressionTags(self, filename_expression):
        tag_parameter_expression = '\?P<(\w+)>'
        return re.findall(tag_parameter_expression, filename_expression)

    def getFileNameInfo(self, filename_expression, base_path = None):
        try:
            id3_tags_to_match = self._getFilenameExpressionTags(filename_expression)
            return self._getFileNameInfo(filename_expression, id3_tags_to_match, base_path)
        except:
            return {}
    
    def setFileNameInfo(self, filename_expression = '(?P<tracknumber>\d+) -? (?P<title>.*).mp3', base_path = None):
        thereWasATagSetted = False
        for key, value in self.getFileNameInfo(filename_expression, base_path).iteritems():
            self.setTag(key, value)
            thereWasATagSetted = True
        return thereWasATagSetted
    
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
        tags = []
        for key in self.id3_data.keys():
            key = key.split(":")[0]
            if mutagen_id3_tags_reversed.get(key):
                tags.append(mutagen_id3_tags_reversed[key])
        return tags
    
    def removeID3TagsNotIn(self, to_mantain_id3_tags):
        mutagen_keys_to_mantain = map(lambda key: mutagen_id3_tags[key], to_mantain_id3_tags)
        actual_id3_elements_to_mantain = {}
        for key, value in self.id3_data.iteritems():
            if key in mutagen_keys_to_mantain:
                actual_id3_elements_to_mantain[key] = value
        self.id3_data.delete()
        for key, value in actual_id3_elements_to_mantain.iteritems():
            self.id3_data.add(value)
    
    def setImage(self, image_path):
        self.id3_data.add(MutagenID3.APIC(3, guess_type(image_path)[0], 3, 'Front cover', open(image_path, 'rb').read()))
    
    def debugTrackInfo(self):
        for tag in self.getTags():
            print "%s: %s" % (tag, self.getTag(tag))
    
    def save(self):
        self.id3_data.save()