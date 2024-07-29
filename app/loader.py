import requests


def is_downloadable(url):
    h = requests.head(url, allow_redirects=True)
    h.raise_for_status()

    content_type = h.headers.get("content-type")

    return content_type and content_type.lower() in (
        "text/csv",
        "application/octet-stream",
    )


def fetch_data(api_url, headers=None, params=None):
    try:
        if is_downloadable(api_url):
            response = requests.get(
                api_url, headers=headers, params=params, stream=True
            )
            response.raise_for_status()

            return response.content.decode("utf-8")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None
