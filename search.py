import sqlite3
from sqlalchemy import MetaData, Table


def get_column_names(table_name, cursor):
    # Use PRAGMA statement to get the column names for a table
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()

    # Extract column names from the result
    column_names = [column[1] for column in columns]

    return column_names


def find_columns(tablename, engine):
    metadata = MetaData()
    metadata.reflect(bind=engine)

    #
    your_table = Table(tablename, metadata, autoload_with=engine)

    # Get column names
    column_names = your_table.columns.keys()
    return column_names


def search_songs(value_name, column_given, table_name="songs"):
    conn = sqlite3.connect("databases/global.db")
    cursor = conn.cursor()

    # Get the column names dynamically
    column_names = get_column_names(table_name, cursor)

    # Build the SELECT query with dynamic column names
    # query = f"SELECT * FROM {table_name} WHERE 'Movie Name' LIKE '%{movie_name}%'"
    cursor.execute(f'select * from songs where "{column_given}" LIKE "%{value_name}%"')

    result = cursor.fetchall()

    # if result:
    #
    #     for row in result:
    #         for i in range(len(column_names)):
    #             if row[i] is not None:
    #                 print(f"{column_names[i]}: {row[i]}")
    #         print("\n")
    # else:
    #     print(f"No matching records found for the {column_given}:", value_name)

    cursor.close()
    conn.close()

    return result, column_names  # global_columns


def search_movie(movie_name, table_name):
    conn = sqlite3.connect("databases/global.db")
    cursor = conn.cursor()

    # Get the column names dynamically
    column_names = get_column_names(table_name, cursor)

    # Build the SELECT query with dynamic column names
    # query = f"SELECT * FROM {table_name} WHERE 'Movie Name' LIKE '%{movie_name}%'"
    cursor.execute(
        f'select * from global_table where "Movie Name" LIKE "%{movie_name}%"'
    )

    result = cursor.fetchall()

    # if result:
    #
    #     for row in result:
    #         for i in range(len(column_names)):
    #             if row[i] is not None:
    #                 # print(f"{column_names[i]}: {row[i]}")
    #         # print("\n")
    # else:
    #     print("No matching records found for the movie:", movie_name)

    cursor.close()
    conn.close()
    return result, column_names


if __name__ == "__main__":
    # Example usage
    # table_name_to_search = input("Enter the table name: ")
    table_name_to_search = "global_table"
    movie_name_to_search = input("Enter the movie name to search: ")
    search_movie(movie_name_to_search, table_name_to_search)

    song_tosearch = ""
    column_given = ["S"]

    search_songs(song_tosearch, column_given)
