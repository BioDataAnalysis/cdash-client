import json
import os

config = {}

settings_file_wd = f"{os.getcwd()}/cdash-client.json"
home_directory = os.path.expanduser("~")
settings_file_home = f"{home_directory}/cdash-client.json"
settings_file = ""

# First of all, we look for our settings file inside the user's home folder.
# This is cross-platform. On Windows, it will look into "C:\Users\<User>\cdash-client.json"
if os.path.isfile(settings_file_home) and os.access(settings_file_home, os.R_OK):
    settings_file = settings_file_home
else:
    print("Settings file not found in home directory. Looking in working directory...")
    if os.path.isfile(settings_file_wd) and not os.access(settings_file_wd, os.R_OK):
        settings_file = settings_file_wd
    else:
        raise Exception("Settings file was not found neither in the home directory, or current working directory")

with open(settings_file, "r") as f:
    config = json.load(f)
