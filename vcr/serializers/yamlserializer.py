import sys
import yaml
import six

# Use the libYAML versions if possible
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def _restore_frozenset():
    # Restore __builtin__.frozenset for cassettes serialized
    # in python2 but deserialized in python3
    # (it moved or something)

    if '__builtin__' not in sys.modules:
        import builtins
        sys.modules['__builtin__'] = builtins


def _fix_response_unicode(d):
    if isinstance(d, dict) and isinstance(d.get('body', {}).get('string'), type(u'')):
        d['body']['string'] = d['body']['string'].encode('utf-8')
    return d


def deserialize(cassette_string):
    if six.PY3:
        _restore_frozenset()
    data = yaml.load(cassette_string, Loader=Loader)
    requests = [r['request'] for r in data]
    responses = [_fix_response_unicode(r['response']) for r in data]
    return requests, responses


def serialize(cassette_dict):
    data = ([{
        'request': request,
        'response': response,
    } for request, response in zip(
        cassette_dict['requests'],
        cassette_dict['responses']
    )])
    return yaml.dump(data, Dumper=Dumper)
