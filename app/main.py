import requests
from csv_functions import *
from database import *
from loader import *


response = requests.get(
    "https://drive.usercontent.google.com/download?id=1RJKGrwzznR9wA7rGNM76cRp1Tis7V-Xq&export=download",
    stream=True,
)

open("csv_file.csv", "wb").write(response.content)

# fetch_data(api_url)

file_path = "csv_file.csv"

with open("csv_file.csv", "r") as file:
    name = get_file_name(response.headers.get("content-disposition"))

    dataframe, tbl_name, col_names, col_types = convert_file_to_dataframe(file, name)

    upload_to_db(tbl_name, col_types, file_path, file, dataframe, col_names)
