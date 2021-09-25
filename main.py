#!/usr/bin/python3
from ftplib import FTP
import logging
import json
from os import path
from os.path import exists
from playsound import playsound
import multiprocessing
import pysftp

CACHE_FILE = "cache.json"
logging.basicConfig(filename="gui.log", level=logging.DEBUG)


def connect_sftp(url, user, password, remove_file):
    conn = pysftp.Connection(url, username=user, password=password, cnopts=None)
    conn.cd("~")
    # sftp.get(filename, "audio")
    

    # save_cache(url, user, password, "audio.m4a", remove_file)
    return conn
    
def get_file(conn, filename):
    conn.get(filename, "audio")


def play():
    p = multiprocessing.Process(target=playsound, args=("audio",))
    print(p)
    p.start()
    return p


def save_cache(url, user, password, filename, remove_file):
    obj = {
        "url": url,
        "user": user,
        "password": password,
        "filename": filename,
        "remove_file": remove_file,
    }

    with open(CACHE_FILE, "w") as outfile:
        json.dump(obj, outfile)


def load_cache():
    if not exists(CACHE_FILE):
        return "", "", "", "", True
    with open(CACHE_FILE, "r") as openfile:
        obj = json.load(openfile)

    url, user, password, filename, remove_file = (
        obj["url"],
        obj["user"],
        obj["password"],
        obj["filename"],
        obj["remove_file"],
    )
    return url, user, password, filename, remove_file
