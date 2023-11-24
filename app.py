# Install necessary packages
# pip install streamlit
# pip install sqlite3
import pandas as pd
import streamlit as st
import sqlite3
from hashlib import sha256

GLOBAL_DATABASE = "databases/global.db"


# Function to create a database table
def create_table():  # NOT USABLE
    conn = sqlite3.connect(GLOBAL_DATABASE)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS user (username TEXT, password TEXT)")
    conn.commit()
    conn.close()


# Function to add a new user to the database
def add_user(username, password):
    conn = sqlite3.connect(GLOBAL_DATABASE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO user (username, password) VALUES (?, ?)", (username, password)
    )
    conn.commit()
    conn.close()


# Function to check if a user exists in the database
def user_exists(username):
    conn = sqlite3.connect(GLOBAL_DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM user WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user is not None


# Function to authenticate a user
def authenticate_user(username, password):
    conn = sqlite3.connect(GLOBAL_DATABASE)
    c = conn.cursor()
    c.execute(
        "SELECT * FROM user WHERE username = ? AND password = ?", (username, password)
    )
    user = c.fetchone()
    conn.close()
    return user is not None


# Function to search for users in the database
def search_users(query):
    conn = sqlite3.connect(GLOBAL_DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM user WHERE username LIKE ?", ("%" + query + "%",))
    results = c.fetchall()
    conn.close()
    return results


# Function to search for movies in the database
def search_movies(query):
    conn = sqlite3.connect(GLOBAL_DATABASE)
    table_name = "global_table"
    c = conn.cursor()
    c.execute(f"SELECT * FROM global_table WHERE 'Movie Name' LIKE '%{query}%'")

    results = c.fetchall()
    conn.close()
    return results


from search import search_movie, search_songs


# Streamlit UI
def main():
    st.title("User Authentication App")

    create_table()  # Create the user table if it doesn't exist

    # User Registration
    st.header("User Registration")
    new_username = st.text_input("Enter a new username:")
    new_password = st.text_input("Enter a new password:", type="password")

    if st.button("Register"):
        if new_username and new_password:
            if not user_exists(new_username):
                # hashed_password = sha256(new_password.encode()).hexdigest()
                add_user(new_username, new_password)
                st.success("Registration successful! You can now login.")
            else:
                st.warning(
                    "Username already exists. Please choose a different username."
                )
        else:
            st.warning("Please enter both username and password.")

    # User Login
    st.header("User Login")
    username = st.text_input("Enter your username:")
    password = st.text_input("Enter your password:", type="password")

    if st.button("Login"):
        if username and password:
            # hashed_password = sha256(password.encode()).hexdigest()
            if authenticate_user(username, password):
                st.success("Login successful!")
            else:
                st.warning("Invalid username or password. Please try again.")
        else:
            st.warning("Please enter both username and password.")

    # User Search
    st.header("User Search")
    search_query = st.text_input("Enter a username to search:")
    if st.button("Search"):
        if search_query:
            search_results = search_users(search_query)
            if search_results:
                st.table(search_results)
            else:
                st.info("No matching users found.")
        else:
            st.warning("Please enter a search query.")

    # Movie Search
    st.header("Movie Search")
    movie_query = st.text_input("Enter a movie title to search:")
    if st.button("Find Movie"):
        if movie_query:
            movie_results, global_columns = search_movie(movie_query, "global_table")
            if movie_results:
                # Display the movie results in a pandas DataFrame
                df = pd.DataFrame(movie_results, columns=global_columns)
                st.table(df)
            else:
                st.info("No matching movies found.")
        else:
            st.warning("Please enter a search query for movies.")

    # Song Search
    st.header("Song Search")
    song_query = st.text_input("Enter a search query for songs:")
    search_category = st.selectbox(
        "Choose search category:", ["Song_Name", "Artist_Name", "Album_Name"]
    )

    if st.button("Search Songs"):
        if song_query:
            song_results, global_columns_songs = search_songs(
                song_query, search_category
            )
            if song_results:
                # Display the song results in a pandas DataFrame
                df = pd.DataFrame(song_results, columns=global_columns_songs)
                st.table(df)
            else:
                st.info("No matching songs found.")
        else:
            st.warning("Please enter a search query for songs.")


if __name__ == "__main__":
    main()
