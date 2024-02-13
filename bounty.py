import datetime
from urllib.parse import urlparse
from subprocess import Popen
import eventlet
from flask import Flask

eventlet.monkey_patch()

import redis
import numpy as np

my_application = Flask(__name__)

REDIS_URL = "***********************"
print("REDIS_URL: ", REDIS_URL)

host = urlparse(REDIS_URL).hostname
port = urlparse(REDIS_URL).port
password = urlparse(REDIS_URL).password

try:
    my_application.redis = redis.Redis(
        host=host,
        port=port,
        password=password,
        ssl=True,
        ssl_cert_reqs=None,
    )

    my_application.redis.set("redis", "ready")
except Exception as e:
    print(f"Error: {e}")


@my_application.route("/")
def index():
    # Set a value in Redis
    my_application.redis.set("hello", str(datetime.datetime.now()))
    return "Hello, World!"


if __name__ == "__main__":
    # Use subprocess to start Flask in a separate process
    flask_process = Popen(["python", __file__])
    try:
        my_application.run(debug=True)
    finally:
        flask_process.terminate()
