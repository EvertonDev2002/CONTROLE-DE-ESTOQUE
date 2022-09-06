from os import getenv
from dotenv import load_dotenv

load_dotenv()
if getenv("DEV") == "True":
    env = {
        "URI": getenv("URI"),
        "KEY": getenv("KEY"),
    }
else:
    env = {
        "URI": getenv("URL"),
        "KEY": getenv("KEY"),
    }
