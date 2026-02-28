import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from flask import Flask, jsonify, request as flask_request

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "TVBox 爬虫后端服务", "version": "1.0.0"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

def handler(environ, start_response):
    return app(environ, start_response)
