import json
from flask import Flask, g
from redis_client import RedisClient
app = Flask(__name__)

@app.route("/")
def index():
    return "<h2>hello world</h2>"

def get_conn(website):
    if not hasattr(g, website):
        g.redis = RedisClient("cookies", website)
    return g.redis

@app.route("/lianjia")
def get_lianjia_cookie():
    """
        get cookie
    """
    conn = get_conn("lianjia")
    return conn.get_cookie()
    
    



