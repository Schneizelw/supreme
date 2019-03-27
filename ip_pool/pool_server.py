from flask import Flask, g
from redis_client import RedisClient

__all__ = ["app"]
app = Flask(__name__)

def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis

@app.route('/')
def helloworld():
    return "<h2>hello world<h2>"

@app.route("/proxy")
def get_proxy():
    """
        get proxy
    """
    conn = get_conn()
    return conn.get_highly_proxy()

@app.route("/count")
def get_counts():
    """
        proxy count
    """
    conn = get_conn()
    return str(conn.count())
