#!/usr/bin/python3
from ftplib import FTP
import logging
import json
from os import path
from os.path import exists
from playsound import playsound
import multiprocessing

CACHE_FILE = "cache.json"
logging.basicConfig(filename='gui.log', level=logging.DEBUG)
 
def connect_and_getfile(url, user, password, filename, remove_file):
    try:
        ftpObject = FTP(url);
    except Exception:
        error = "Error connecting to server. Url is wrong or server is down"
        logging.error(error)
        return Exception(error)

    ftpObject.login(user, password);
    ftpObject.retrbinary(f"RETR {filename}", open("audio", 'wb').write);

    save_cache(url, user, password, filename, remove_file)

def play():
    p = multiprocessing.Process(target=playsound, args=('audio', ))
    print(p)
    p.start()
    return p

def save_cache(url, user, password, filename, remove_file):
    obj = {
            "url": url,
            "user": user,
            "password": password,
            "filename": filename,
            "remove_file": remove_file
        }

    with open(CACHE_FILE, "w") as outfile:
            json.dump(obj, outfile)

def load_cache():
    if not exists(CACHE_FILE):
        return "", "", "", "", ""
    with open(CACHE_FILE, 'r') as openfile:
        obj = json.load(openfile)

    url, user, password, filename, remove_file = obj["url"], obj["user"], obj["password"], obj["filename"], obj["remove_file"]
    return url, user, password, filename, remove_file



