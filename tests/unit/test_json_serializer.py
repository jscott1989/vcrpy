import pytest
from vcr.serializers.jsonserializer import serialize
from vcr.request import Request


def test_serialize_binary():
    request = Request('http','localhost',80,'GET','/',{},{})
    cassette = {'requests': [request], 'responses': [{'body':b'\x8c'}]}

    with pytest.raises(Exception) as e:
        serialize(cassette)
        assert e.message == "Error serializing cassette to JSON. Does this \
            HTTP interaction contain binary data? If so, use a different \
            serializer (like the yaml serializer) for this request"
