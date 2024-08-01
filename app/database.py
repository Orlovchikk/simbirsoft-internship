import os
import psycopg2
from io import StringIO
from dotenv import load_dotenv
from app.logger import logger


load_dotenv()

host = os.getenv("host")
dbname = os.getenv("POSTGRES_DB")
user = os.getenv("PGUSER")
password = os.getenv("POSTGRES_PASSWORD")
port = os.getenv("port")


def upload_to_db(table_name, col_types, dataframe, col_names):
    logger.info(f"Connecting to database: {dbname}")
    try:
        conn = psycopg2.connect(
            host=host, user=user, password=password, dbname=dbname, port=port
        )
        cursor = conn.cursor()
        logger.info(f"Connected successfully")
    except psycopg2.Error as e:
        logger.error(f"Error connecting to database: {e}")
        return

    try:
        logger.info(f"Starting data loading process to table: {table_name}")
        cursor.execute("DROP TABLE IF EXISTS {};".format(table_name))
        cursor.execute("CREATE TABLE {} ({});".format(table_name, col_types))

        output = StringIO()
        dataframe.to_csv(
            output, sep=",", header=col_names, index=False, encoding="utf-8"
        )
        output.seek(0)

        sql_statment = "COPY {} FROM STDIN WITH CSV HEADER DELIMITER AS ',';".format(
            table_name
        )
        cursor.copy_expert(sql=sql_statment, file=output)

        cursor.execute("GRANT SELECT ON TABLE {} TO PUBLIC;".format(table_name))

        conn.commit()
        logger.info(f"Data successfully uploaded to table '{table_name}'")

    except psycopg2.Error as e:
        logger.error(f"Error during database operation: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
