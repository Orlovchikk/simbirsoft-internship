from io import StringIO
import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()

host = os.getenv("host")
dbname = os.getenv("POSTGRES_DB")
user = os.getenv("PGUSER")
password = os.getenv("POSTGRES_PASSWORD")
port = os.getenv("port")


def upload_to_db(table_name, col_types, dataframe, col_names):
    conn = psycopg2.connect(
        host=host, user=user, password=password, dbname=dbname, port=port
    )
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS {};".format(table_name))
    cursor.execute("CREATE TABLE {} ({});".format(table_name, col_types))

    output = StringIO()
    dataframe.to_csv(output, sep=",", header=col_names, index=False, encoding="utf-8")
    output.seek(0)

    sql_statment = "COPY {} FROM STDIN WITH CSV HEADER DELIMITER AS ',';".format(
        table_name
    )
    cursor.copy_expert(sql=sql_statment, file=output)

    cursor.execute("GRANT SELECT ON TABLE {} TO PUBLIC;".format(table_name))

    conn.commit()

    cursor.close()
    conn.close()

    return
