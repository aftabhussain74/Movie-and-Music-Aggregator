import sqlite3
from sqlalchemy import create_engine, inspect, MetaData, Table
from fuzzywuzzy import fuzz

# import sqlalchemy

import os
import pandas as pd

list_of_db = [
    # "databases/amazon_music.db",
    "databases/amdc",
    # "databases/itunes.db",
    "databases/movielens.db",
    "databases/movies1.db",
    "databases/movies2.db",
    "databases/movies3.db",
    "databases/movies4.db",
    "databases/movies5.db",
    "databases/movies_metadata.db",
    # "databases/msd.db",
    "databases/tmdb.db",
    "databases/tsv_db",
]


def extract(list_of_db: list):
    list_of_conn = []

    for db in list_of_db:
        list_of_conn.append(create_engine(f"sqlite:///{db}"))

    # queries = []

    list_of_tables = []

    for db in list_of_db:
        inspector = inspect(db)
        table_names = inspector.get_table_names()
        for table in table_names:
            queries = pd.read_sql(f"Select * from {table}")


def find_matching_columns(global_columns, local_columns):
    matches = {}
    reverse_matches = {}
    for global_column in global_columns:
        for local_column in local_columns:
            similarity_score = fuzz.token_set_ratio(global_column, local_column)
            if "title" in local_column.lower():
                matches["Movie Name"] = local_column
                reverse_matches[local_column] = "Movie Name"

            elif similarity_score > 70:
                # if global_column not in matches:
                # matches[global_column] = []
                matches[global_column] = local_column
                reverse_matches[local_column] = global_column
    return matches, reverse_matches


def get_all_tables(engine):

    # Reflect the existing database schema
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Get a list of all table names
    table_names = metadata.tables.keys()

    return table_names


def find_columns(tablename, engine):
    metadata = MetaData()
    metadata.reflect(bind=engine)

    #
    your_table = Table(tablename, metadata, autoload_with=engine)

    # Get column names
    column_names = your_table.columns.keys()
    return column_names


def load_in_global(local, g):
    # db_name = "simple_ui_db.db"
    #
    # local = create_engine(f"sqlite:///databases/{db_name}")  # change
    # g = create_engine("sqlite:///databases/global.db")

    global_columns = find_columns("songs", g)  # global tablename
    # tablename = "m3_imdb"
    tableslist = list(get_all_tables(local))
    # tableslist =
    for tablename in tableslist:
        print(f"{tablename} Table in progress...")
        local_columns = find_columns(tablename, local)  # change

        matches, reversed_matches = find_matching_columns(global_columns, local_columns)

        df = pd.read_sql(f"select * from {tablename}", local)
        new_df = pd.DataFrame(columns=global_columns)
        # new_df.columns = global_columns
        for index, row in df.iterrows():
            column_list = []
            for column in global_columns:
                if column in matches.keys():
                    column_list.append(matches[column])
            new_row = row[column_list]
            new_dict = {}
            for i in new_row.keys():
                new_dict[reversed_matches[i]] = new_row[i]
            # new_df = new_df.append(new_dict, ignore_index=True)
            # Get the index for the new row
            new_index = len(new_df)

            # Insert the new row into the DataFrame
            new_df.loc[new_index] = new_dict

        new_df.to_sql("songs", g, if_exists="append", index=False)
        print(f"{tablename} table completed!")
        # print(new_dict)
        # print(new_row)
        # print("\n")


if __name__ == "__main__":
    local_db_name = "databases/msd.db"

    local_engine = create_engine(f"sqlite:///{local_db_name}")  # change
    global_engine = create_engine("sqlite:///databases/global.db")

    load_in_global(local_engine, global_engine)
