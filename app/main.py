import sys
from io import StringIO

from csv_functions import *
from database import *
from loader import *


if __name__ == "__main__":

    def main(api_url):
        # logging.info(f"Starting data loading process for URL: {api_url}")

        # try:
        response = fetch_data(api_url)

        csv_data = StringIO(response.text)
        name = get_file_name(response.headers.get("content-disposition"))

        dataframe, tbl_name, col_names, col_types = convert_file_to_dataframe(
            csv_data, name
        )

        upload_to_db(tbl_name, col_types, dataframe, col_names)

    # except requests.exceptions.RequestException as e:
    # logging.error(f"Error fetching data from API: {e}")
    # except Exception as e:
    # logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <api_url>")
        sys.exit(1)

    url = sys.argv[1]
    main(url)
