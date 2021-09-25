#!/usr/bin/python3
from ftplib import FTP
import logging
import sys
import json
from os import path
from os.path import exists
from playsound import playsound
from audioplayer import AudioPlayer
import multiprocessing
import pysftp

if sys.platform == "win32":
    import winsound

CACHE_FILE = "cache.json"
logging.basicConfig(filename="gui.log", level=logging.DEBUG)


def connect_sftp(url, user, password, remove_file):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    conn = pysftp.Connection(url, username=user, password=password, cnopts=cnopts)
    conn.cd("~")
    save_cache(url, user, password, remove_file)
    return conn
    
def get_file(conn, filename):
    conn.get(filename, "audio")


def play():
    
    if sys.platform == "win32":
        p = multiprocessing.Process(target=winsound.PlaySound, args=("audio", winsound.SND_FILENAME))
    else:
        p = multiprocessing.Process(target=playsound, args=("audio",))
    p.start()
    return p


def save_cache(url, user, password, remove_file):
    obj = {
        "url": url,
        "user": user,
        "password": password,
        "remove_file": remove_file,
    }

    with open(CACHE_FILE, "w") as outfile:
        json.dump(obj, outfile)


def load_cache():
    if not exists(CACHE_FILE):
        return "", "", "", "", True
    with open(CACHE_FILE, "r") as openfile:
        obj = json.load(openfile)

    url, user, password, remove_file = (
        obj["url"],
        obj["user"],
        obj["password"],
        obj["remove_file"],
    )
    return url, user, password, remove_file
