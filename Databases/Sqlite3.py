import discord
import Constant
import sqlite3

class Sqlite3():

    def __init__(self):
        DB_NAME = "hashchag"
        db_path = os.path.join(os.path.abspath(os.getcwd()), DB_NAME + ".db")
        self.db = sqlite3.connect(db_path)
        self.db_cursor = self.db.cursor()
        self.db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS guilds (
            id INTEGER PRIMARY KEY,
            name TEXT,
        ),
        CREATE TABLE IF NOT EXISTS bans (
            id INTEGER PRIMARY KEY,
            ban_id INTEGER,
            foreign key (id) references guilds(id)
        ),
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY,
            name TEXT,
            foreign key (id) references guilds(id)
        ),
        """)