from json import JSONEncoder, JSONDecoder
import json

from musiclang import Score, Melody, Chord, Note
from musiclang.library import *


class MusicLangEncoder(JSONEncoder):
    def default(self, obj):

        if isinstance(obj, (Score, Melody, Chord, Note)):
            return {'_type': "score", '_val': str(obj)}
        return super(MusicLangEncoder, self).default(obj)


class MusicLangDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if '_type' not in obj:
            return obj
        type = obj['_type']
        if type == 'score':
            score = eval(obj['_val'].replace('\n', ''))
            return score
        return obj