from urllib.parse import urlparse


def is_valid_url(text):
    try:
        result = urlparse(text)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def create(query, variables):
    payload = {
        'query': query,
        'variables': variables
    }
    return payload
