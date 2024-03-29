import datetime
from urllib.parse import urlparse
import eventlet
from flask import Flask

eventlet.monkey_patch()

import redis
import numpy as np

my_application = Flask(__name__)

# Feel free to test with this
REDIS_URL = "rediss://:pbe6272829f62aa1f18c6ee4f8f55456aa71d044a75ca069a3b5f6b6963971b56@ec2-46-137-49-233.eu-west-1.compute.amazonaws.com:27779"
print("REDIS_URL: ", REDIS_URL)

host = urlparse(REDIS_URL).hostname
port = urlparse(REDIS_URL).port
password = urlparse(REDIS_URL).password

try:
    # Wrap Redis connection code inside a context manager
    with eventlet.Timeout(5, False):  # Set a timeout for the Redis connection
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
    my_application.run(debug=True)
