from flask import send_from_directory, Flask
import os
import asyncio

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory(os.path.dirname(__file__), 'index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.dirname(__file__), 'favicon.ico')

@app.route('/style.css')
def css():
    return send_from_directory(os.path.dirname(__file__), 'style.css')

@app.route('/img.png')
def img():
    return send_from_directory(os.path.dirname(__file__), 'img.png')



def stop():
    os._exit(0)

async def run():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, app.run, 'localhost', 8080)

def keep_alive():
    asyncio.run(run())

keep_alive()
