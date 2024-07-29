import pandas as pd
import re


def convert_file_to_dataframe(csv_file, name):
    dataframe = pd.read_csv(csv_file, sep=None, engine="python")

    table_name = format_str(name)

    dataframe.columns = [format_str(col) for col in dataframe.columns]

    columns_types = get_col_dtypes(dataframe)

    return dataframe, table_name, dataframe.columns, columns_types


def get_file_name(headers):
    if not headers:
        return None

    file_name = re.findall('filename="(.*)"', headers, re.IGNORECASE)

    if len(file_name) == 0:
        return None
    return file_name[0][:-4]


def format_str(str):
    return (
        str.lower()
        .strip()
        .replace(" ", "_")
        .replace("$", "")
        .replace("%", "")
        .replace("-", "_")
        .replace(r"/", "_")
        .replace("\\", "_")
        .replace("<", "")
        .replace(">", "")
    )


def get_col_dtypes(dataframe):
    converting = {
        "timedelta64[ns]": "varchar",
        "object": "varchar",
        "float64": "float",
        "int64": "int",
        "datetime64": "timestamp",
    }

    return ", ".join(
        f"{n} {d}"
        for (n, d) in zip(dataframe.columns, dataframe.dtypes.replace(converting))
    )
