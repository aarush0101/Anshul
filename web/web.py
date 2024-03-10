import flask
from flask import send_from_directory
import os
import sys
from threading import Thread

app = flask.Flask(__name__)


@app.route('/')
@app.route('/<path:filename>')
def index(filename=None):
    if filename:
        # Serve static files directly
        return send_from_directory(os.path.abspath(os.path.dirname(__file__)), filename)

    html_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'index.html')
    with open(html_file_path, 'r') as file:
        html_content = file.read()
    return html_content

def stop():
    os._exit(0)

def run():
    app.run(host='localhost', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()