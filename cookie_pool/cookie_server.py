import json
from flask import Flask, g
from redis_client import RedisClient
app = Flask(__name__)

@app.route("/")
def index():
    return "<h2>hello world</h2>"

def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient("cookies","qfang")
    return g.redis

@app.route("/cookie")
def get_cookie():
    """
        get cookie
    """
    conn = get_conn()
    return conn.get_cookie()
    


