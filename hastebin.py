'''
File for debugging items and information for easy access.
'''

import requests
import os
import re


ab_path = os.path.join(os.path.dirname(__file__), 'temp')
log_file = os.path.join(ab_path, 'log.log')


def remove_ansi_escape_codes(text):
    """
    Uses regex to remove ansi escape codes from logs
    """
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)
    
def get_logs():
    """
    Read the latest logs from temp.log.log and compile to remove ansi codes.
    """
    with open(log_file, 'r') as f:
        data = f.read()
    global complied_data
    complied_data = remove_ansi_escape_codes(data)


def hastebin():
    """
    Returns str, no parameters taken
    """
    try:
        get_logs()  # Call the get_logs function to prepare the log data
        url = requests.post("https://hastebin.cc/documents", data=complied_data)
        json = url.json()
        haste_key = json['key']
        url = "https://hastebin.cc/" + haste_key
        return url
    except Exception as e:
        logs.LoggerDSC("inf", f"HasteBin debugging failed. Uncaught Exception: {e}")
        return e

