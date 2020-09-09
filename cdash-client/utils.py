import os
from settings import config

def is_server_up():
    return os.system(f"ping -c 1 {config['cdash_server']['hostname']} > /dev/null 2>&1")
