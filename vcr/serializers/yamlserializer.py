import sys
import yaml
import six
from . import compat

# Use the libYAML versions if possible
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def _restore_frozenset():
    """
    Restore __builtin__.frozenset for cassettes serialized in python2 but 
    deserialized in python3 (it moved or something)
    """

    if '__builtin__' not in sys.modules:
        import builtins
        sys.modules['__builtin__'] = builtins

def deserialize(cassette_string):
    if six.PY3:
        _restore_frozenset()
    data = yaml.load(cassette_string, Loader=Loader)
    requests = [r['request'] for r in data]
    responses = [r['response'] for r in data]
    responses = [compat.convert_body_to_bytes(r['response']) for r in data]
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
