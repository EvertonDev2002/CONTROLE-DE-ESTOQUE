from os import getenv
from dotenv import load_dotenv

load_dotenv()

env = {
    "URI": getenv("URI"),
    "KEY": getenv("KEY"),
    "HEROKU": getenv("URL"),
}
