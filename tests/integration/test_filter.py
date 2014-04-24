import base64
from six.moves.urllib.request import urlopen, Request
import vcr


def _request_with_auth(url, username, password):
    request = Request(url)
    base64string = base64.b64encode(username.encode('ascii') + b':' + password.encode('ascii'))
    request.add_header(b"Authorization", b"Basic " + base64string)
    return urlopen(request)


def _find_header(cassette, header):
    for request in cassette.requests:
        for k, v in request.headers:
            if header.lower() == k.lower():
                return True
    return False


def test_filter_basic_auth(tmpdir):
    url = 'http://httpbin.org/basic-auth/user/passwd'
    with vcr.use_cassette(str(tmpdir.join('basic_auth_filter.yaml')), filter_headers=['authorization']) as cass:
        resp = _request_with_auth(url, 'user', 'passwd')
        assert resp.getcode() == 200
        assert not _find_header(cass, 'authorization')


def test_filter_querystring(tmpdir):
    url = 'http://httpbin.org/?foo=bar'
    with vcr.use_cassette(str(tmpdir.join('basic_auth_filter.yaml')), filter_query_parameters=['foo']) as cass:
        urlopen(url)
        assert not 'foo' in cass.requests[0].url
