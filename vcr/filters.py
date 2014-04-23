from six.moves.urllib.parse import urlparse, parse_qsl, urlunparse

def _remove_headers(request, headers_to_remove):
    out = []
    for k, v in request.headers:
        if k.lower() not in [h.lower() for h in headers_to_remove]:
            out.append((k, v))
    request.headers = frozenset(out)
    return request


def _remove_query_parameters(request, query_parameters_to_remove):
    for query_parameter_to_remove in query_parameters_to_remove:
        url = urlparse(request.url)
        q = parse_qsl(url.query)
        q = [(k, v) for k,v in q if k not in query_parameter_to_remove]
        new_url = urlunparse((
            url.scheme,
            url.netloc,
            url.path,
            url.params,
            q,
            url.fragment,
        ))
        new_path = urlparse(new_url).path
        request.path = new_path

    return request


def filter_request(request, filter_headers, filter_query_parameters):
    if hasattr(request, 'headers'):
        request = _remove_headers(request, filter_headers)
    request = _remove_query_parameters(request, filter_query_parameters)
    return request
