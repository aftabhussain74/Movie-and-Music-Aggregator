import sqlite3
import csv
import os
import pandas as pd

db_name = "movies5.db"
csv_file_path = "data/movies5/imdb.csv"
table_name = "m5_imdb"


def create_db_from_csv(csv_file, db_name, table_name):
    # Connect to the SQLite database
    db_path = os.path.join("databases/", f"{db_name}.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Read the CSV file and insert into the SQLite database
        with open(csv_file, "r", encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)  # Read the headers

            # Create the table using the headers from the CSV file
            columns = ", ".join([f'"{col}" TEXT' for col in headers])
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
            cursor.execute(create_table_query)

            # Insert data into the table
            insert_query = (
                f"INSERT INTO {table_name} VALUES ({', '.join(['?']*len(headers))})"
            )
            cursor.executemany(insert_query, csv_reader)

        conn.commit()  # Commit the changes
        print(
            f"Data from '{csv_file}' imported successfully into the '{db_name}' database as table '{table_name}'."
        )
    except Exception as e:
        conn.rollback()  # Rollback in case of an error
        print("An error occurred:", e)
    finally:
        conn.close()  # Close the connection

def create_db_from_tsv(tsv_file, db_name, table_name):
    # Read TSV file into a pandas DataFrame
    df = pd.read_csv(tsv_file, sep=',' , encoding='utf-8', on_bad_lines='warn')

    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)

    try:
        # Write the DataFrame to SQLite database
        df.to_sql(table_name, conn, if_exists='replace', index=False)

        print(f"Data from '{tsv_file}' imported successfully into the '{db_name}' database as table '{table_name}' using pandas.")
    except Exception as e:
        print("An error occurred:", e)
    finally:
        conn.close()  # Close the connection

if __name__ == '__main__':

    # create_db_from_csv(csv_file=csv_file_path, db_name=db_name, table_name=table_name)
    create_db_from_tsv(csv_file_path, db_name, table_name)