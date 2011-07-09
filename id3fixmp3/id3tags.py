mutagen_id3_tags = {
    'album': 'TALB',
    'bpm': 'TBPM',
    'compilation': 'TCMP', # iTunes extension
    'composer': 'TCOM',
    'copyright': 'TCOP',
    'encodedby': 'TENC',
    'lyricist': 'TEXT',
    'length': 'TLEN',
    'media': 'TMED',
    'mood': 'TMOO',
    'title': 'TIT2',
    'version': 'TIT3',
    'artist': 'TPE1',
    'performer': 'TPE2', 
    'conductor': 'TPE3',
    'arranger': 'TPE4',
    'discnumber': 'TPOS',
    'organization': 'TPUB',
    'tracknumber': 'TRCK',
    'author': 'TOLY',
    'albumartistsort': 'TSO2', # iTunes extension
    'albumsort': 'TSOA',
    'composersort': 'TSOC', # iTunes extension
    'artistsort': 'TSOP',
    'titlesort': 'TSOT',
    'isrc': 'TSRC',
    'discsubtitle': 'TSST',
    'year': 'TDRC',
    'genre': 'TCON',
    'trackposition': 'TPOS',
    'comment': 'COMM',
    'lyrics': 'USLT',
    'image': 'APIC'    
}

mutagen_id3_tags_reversed = {}
for key, value in mutagen_id3_tags.iteritems():
    mutagen_id3_tags_reversed[value] = key