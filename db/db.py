from os.path import isfile
from sqlite3 import connect
from apscheduler.triggers.cron import CronTrigger
from utils import log
import asyncio

DB_PATH = "./data/database.db"
BUILD_PATH = "./db/build.sql"

connection = connect(DB_PATH, check_same_thread=False)
cursor = connection.cursor()

def build():
    if isfile(BUILD_PATH):
        scriptexec(BUILD_PATH)
        log.build(BUILD_PATH)

def commit():
    connection.commit()

def autosave(sched):
    sched.add_job(commit, CronTrigger(second=0))

def close():
    connection.close()

def field(command, *values):
    cursor.execute(command, tuple(values))

    if (fetch := cursor.fetchone()) is not None:
        return fetch[0]

def record(command, *values):
    cursor.execute(command, tuple(values))

    return cursor.fetchone()

def records(command, *values):
    cursor.execute(command, tuple(values))

    return cursor.fetchall()

def column(command, *values):
    cursor.execute(command, tuple(values))

    return [item[0] for item in cursor.fetchall()]

def execute(command, *values):
    cursor.execute(command, tuple(values))

def multiexec(command, valueset):
    cursor.executemany(command, valueset)

def scriptexec(path):
    with open(path, "r", encoding="utf-8") as script:
        cursor.executescript(script.read())
