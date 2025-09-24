import os # allows you to interact with files (create folders)
import requests # download files from the internet
import zipfile # allows you to work with zip files


download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    #"https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip"
    # The URL mentioned doesn't work, so we won't be using it for now and will talk to the provider.
]


DOWNLOAD_DIR = "downloads"


# creates the folder if it doesn't exist
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)


# download and unzip each file
for url in download_uris:
    filename = url.split("/")[-1] # takes the last part of the URL as the file name
    filepath = os.path.join(DOWNLOAD_DIR, filename) # path where it will be saved


    # download file
    r = requests.get(url) # get the data from the zip
    with open(filepath, "wb") as f: # create a file
        f.write(r.content) # save the contents of the zip to the file


    # unzip
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(DOWNLOAD_DIR)


    # delete zip
    os.remove(filepath)


    print(f"{filename} downloaded and unzipped")