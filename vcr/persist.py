from .persisters.filesystem import FilesystemPersister

def _check_for_old_cassette(cassette):
    requests, responses = cassette
    if requests and not hasattr(requests[0], 'uri'):
        raise Exception("Your cassette files were generated in an older version of VCR.  Delete your cassettes or run the migration script. See http://git.io/mHhLBg for more")


def load_cassette(cassette_path, serializer):
    with open(cassette_path) as f:
        cassette = serializer.deserialize(f.read())
        _check_for_old_cassette(cassette)
        return cassette


def save_cassette(cassette_path, cassette_dict, serializer):
    data = serializer.serialize(cassette_dict)
    FilesystemPersister.write(cassette_path, data)
