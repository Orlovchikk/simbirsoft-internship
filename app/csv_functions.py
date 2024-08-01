import pandas as pd
import re
from app.logger import logger


def convert_file_to_dataframe(csv_data, name):
    logger.info(f"Converting data to DataFrame")
    try:
        dataframe = pd.read_csv(csv_data, sep=None, engine="python")
    except (pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        logger.error(f"Error reading CSV data: {e}")
        return None, None, None, None

    table_name = format_str(name)
    dataframe.columns = [format_str(col) for col in dataframe.columns]
    columns_types = get_col_types(dataframe)

    logger.info(f"Data converted successfully")
    return dataframe, table_name, dataframe.columns, columns_types


def get_file_name(headers):
    if not headers:
        return None

    file_name = re.findall('filename="(.*)"', headers, re.IGNORECASE)

    if len(file_name) == 0:
        return None

    name = file_name[0][:-4]
    logger.info(f"Extracted table name: {name}")
    return name


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


def get_col_types(dataframe):
    converting = {
        "timedelta64[ns]": "varchar",
        "object": "varchar",
        "float64": "float",
        "int64": "int",
        "datetime64": "timestamp",
    }

    col_types = []

    for col_name, dtype in zip(dataframe.columns, dataframe.dtypes):
        if str(dtype) == "int64":
            max_val = dataframe[col_name].max()
            if max_val > 2147483647:
                sql_dtype = "bigint"
            else:
                sql_dtype = "int"
        else:
            sql_dtype = converting.get(str(dtype), "varchar")

        col_types.append(f'"{col_name}" {sql_dtype}')

    return ", ".join(col_types)
