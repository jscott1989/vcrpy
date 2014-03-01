import six

def convert_body_to_bytes(resp):
    """
    If the request body is a string, encode it to bytes (for python3 support)

    By default yaml serializes to utf-8 encoded bytestrings.
    When this cassette is loaded by python3, it's automatically decoded
    into unicode strings.  This makes sure that it stays a bytestring, since
    that's what all the internal httplib machinery is expecting.

    For more info on py3 yaml: http://pyyaml.org/wiki/PyYAMLDocumentation#Python3support
    """
    try:
        if not isinstance(resp['body']['string'], six.binary_type):
            resp['body']['string'] = resp['body']['string'].encode('utf-8')
    except (KeyError, TypeError):
        # The thing we were converting either wasn't a dictionary or didn't have
	# the keys we were expecting.  Some of the tests just serialize and
	# deserialize a string.
        pass
    return resp
