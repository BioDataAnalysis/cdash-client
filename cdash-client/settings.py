import json
import os

config = {}

with open(os.path.dirname(__file__) + "/../settings.json", "r") as f:
    config = json.load(f)
