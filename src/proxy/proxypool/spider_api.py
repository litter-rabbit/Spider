from flask import Flask, g

from proxypool.redis_db import RedisClient

__all__ = ['app']

app = Flask(__name__)






"""
    连接redis

"""


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index():
    return '<h2>代理池</h2>'

@app.route('/random')
def get_proxy():
    """

    """
    conn = get_conn()
    return conn.random()


@app.route('/count')
def get_counts():
    """

    """
    conn = get_conn()
    return str(conn.count())


if __name__ == '__main__':
    app.run()
