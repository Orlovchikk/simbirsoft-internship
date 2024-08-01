import requests
from app.logger import logger


def is_downloadable(url):
    try:
        logger.debug(f"Checking if URL is downloadable: {url}")
        h = requests.head(url, allow_redirects=True)
        h.raise_for_status()

        content_type = h.headers.get("content-type")

        if content_type.lower() in ("text/csv" "application/octet-stream"):
            logger.debug("URL is downloadable")
            return content_type

    except requests.exceptions.RequestException as e:
        logger.error(f"URL is not downloadable '{url}': {e}")
        return False


def fetch_data(api_url, headers=None, params=None):
    logger.info(f"Attempting to fetch data from: {api_url}")
    if is_downloadable(api_url):
        try:
            response = requests.get(
                api_url, headers=headers, params=params, stream=True
            )

            logger.info("Data fetched successfully")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from API: {e}")

    else:
        return None
