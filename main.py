import sys
from io import StringIO

from app.csv_functions import convert_file_to_dataframe, get_file_name
from app.database import upload_to_db
from app.loader import fetch_data
from app.logger import logger


def main(api_url):
    logger.info(f"Starting data loading process for URL: {api_url}")

    try:
        response = fetch_data(api_url)

        if response is None:
            logger.error("Failed to fetch data. Exiting.")
            return

        try:
            csv_data = StringIO(response.text)
            name = get_file_name(response.headers.get("content-disposition"))

            dataframe, tbl_name, col_names, col_types = convert_file_to_dataframe(
                csv_data, name
            )

            if dataframe is None:
                logger.error("Failed to create Dataframe. Exiting")
                return

            upload_to_db(tbl_name, col_types, dataframe, col_names)

            logger.info("Data loading process completed.")

        except (AttributeError, ValueError) as e:
            logger.error(f"Error processing data: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

    return


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <api_url>")
        sys.exit(1)

    url = sys.argv[1]
    main(url)
