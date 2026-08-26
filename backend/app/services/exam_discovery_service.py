import requests


def fetch_website(url):

    response = requests.get(
        url,
        timeout=20
    )

    response.raise_for_status()

    return response.text