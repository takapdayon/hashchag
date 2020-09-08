import os
import discord
import Constant
import sqlite3

class Sqlite3():

    def __init__(self):
        DB_NAME = "hashchag"
        db_path = os.path.join(os.path.abspath(os.getcwd()), DB_NAME + ".db")
        self.db = sqlite3.connect(db_path)
        self.db_cursor = self.db.cursor()
        try:
            self.db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS guilds (
                id INTEGER PRIMARY KEY,
                name TEXT)
            """)
            self.db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS bans (
                id INTEGER PRIMARY KEY,
                ban_id INTEGER,
                foreign key (id) references guilds(id))
            """)
            self.db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY,
                name TEXT,
                foreign key (id) references guilds(id))
            """)
        except sqlite3.Error as e:
            print(e.args[0])

    # DBのcommit, closeの凸凸
    def deco(func):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
                self.db.commit()
                self.db.close()
            except sqlite3.Error as e:
                print(e.args[0])
        return wrapper

    @deco
    def addGuild(self, id, name):
        #DBにguild追加
        self.db_cursor.execute(f"INSERT INTO tags VALUES ({id}, {name})")

    @deco
    def addban(self, id, ban_id):
        #DBにguild指定のBANguild追加
        self.db_cursor.execute(f"INSERT INTO tags VALUES ({id}, {ban_id})")

    @deco
    def addTag(self, id, tags):
        #DBにtag追加
        self.db_cursor.execute(f"INSERT INTO tags VALUES ({id}, {tags})")

    @deco
    def deleteTags(self, id, tags):
        self.db_cursor.execute(f"INSERT INTO tags VALUES ({id}, {tags})")


    def showHashTags():
        self.db_cursor.execute('SELECT distinct name FROM tags')
        return db_cursor.fetchall()
