import base64
import codecs
import json

from Util.DefaultProfile import DefaultProfile

def test_DefaultProfile_exists():
    assert DefaultProfile is not None

def test_DefaultProfile_base64():
    zipstring = base64.b64decode(DefaultProfile)
    assert zipstring is not None

def test_DefaultProfile_zlib():
    zipstring = base64.b64decode(DefaultProfile)
    jsonstring = codecs.decode(zipstring, 'zlib')
    assert jsonstring is not None

def test_DefaultProfile_json_is_correct():
    zipstring = base64.b64decode(DefaultProfile)
    jsonstring = codecs.decode(zipstring, 'zlib')
    defaultprofile = json.loads(jsonstring)
    assert defaultprofile is not None
    assert 'General' in defaultprofile
    assert 'Primary' in defaultprofile['General']
    assert defaultprofile['General']['Primary'] == 'Archery'
