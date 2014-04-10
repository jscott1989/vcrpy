def method(r1, r2):
    return r1.method == r2.method


def uri(r1, r2):
    return r1.uri == r2.uri


def host(r1, r2):
    return r1.host == r2.host


def scheme(r1, r2):
    return r1.scheme == r2.scheme


def port(r1, r2):
    return r1.port == r2.port


def path(r1, r2):
    return r1.path == r2.path


def query(r1, r2):
    return r1.query == r2.query


def body(r1, r2):
    return r1.body == r2.body


def headers(r1, r2):
    return r1.headers == r2.headers


def requests_match(r1, r2, matchers):
    return all(m(r1, r2) for m in matchers)
