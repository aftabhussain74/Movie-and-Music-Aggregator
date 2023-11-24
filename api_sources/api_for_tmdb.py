import requests
import json

# import API_KEY

# CONFIDENTAIL
API_KEY = "7daab8d63cc4ff353fc332fd733f7d5e"
API_READ_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3ZGFhYjhkNjNjYzRmZjM1M2ZjMzMyZmQ3MzNmN2Q1ZSIsInN1YiI6IjY1MTkyNDM4YzUwYWQyMDBjOTFiNjk5YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.-WOBYdHUXSLOP2IpoIbBHSpQKptBqe2LnPEfCDP11fo"


api_key = API_KEY
base_url = "https://api.themoviedb.org/3/"

# Specify the movie you want to search for
movie_title = "Inception"

# Construct the full URL with parameters
url = f"{base_url}search/movie?api_key={api_key}&query={movie_title}"

# Make the API request
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(data.keys())
    print(data)
    # Using json.dump() to write data to the file
    file_name = "../inception.json"
    with open(file_name, "w") as json_file:
        json.dump(data, json_file, indent="\t")

    # Process and use the data as needed
else:
    print(f"Error: {response.status_code}")
    # Handle the error


# Output of this code is presented in  inception.json
