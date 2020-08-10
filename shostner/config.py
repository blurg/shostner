from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

config = Config(".env")

MAX_CONNECTIONS_COUNT = int(config("MAX_CONNECTIONS_COUNT", default=10))
MIN_CONNECTIONS_COUNT = int(config("MIN_CONNECTIONS_COUNT", default=10))
SECRET_KEY = Secret(config("SECRET_KEY", default="secret key for project"))

PROJECT_NAME = config("PROJECT_NAME", default="FastAPI example application")
ALLOWED_HOSTS = CommaSeparatedStrings(config("ALLOWED_HOSTS", default=""))

MONGODB_URL = config("DB", default="")  # deploying without docker-compose

database_name = "shostner"

DEFAULT_URL="http://jlugao.com"