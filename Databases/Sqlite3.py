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
                id INTEGER,
                ban_id INTEGER,
                PRIMARY KEY(id, ban_id),
                foreign key (id) references guilds(id))
            """)
            self.db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER,
                name TEXT,
                PRIMARY KEY(id, name),
                foreign key (id) references guilds(id))
            """)
        except sqlite3.Error as e:
            print(e.args[0])

    def __del__(self):
        self.db.commit()
        self.db.close()


    def exception(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(e.args[0])
        return wrapper

    @exception
    def addGuild(self, id, name):
        #DBにguild追加
        self.db_cursor.execute(f"INSERT INTO guilds VALUES ({id}, '{name}')")

    @exception
    def addBan(self, id, ban_id):
        #DBにguild指定のBANguild追加
        self.db_cursor.execute(f"INSERT INTO bans VALUES ({id}, '{ban_id}')")

    @exception
    def addTag(self, id, tag):
        #DBにtag追加
        self.db_cursor.execute(f"INSERT INTO tags VALUES ({id}, '{tag}')")

    @exception
    def deleteGuild(self, id):
        self.db_cursor.execute(f"DELETE FROM guilds where id={id}")

    @exception
    def deleteBan(self, id, ban_id):
        self.db_cursor.execute(f"DELETE FROM bans where id={id} and ban_id={ban_id}")

    @exception
    def deleteTag(self, id, tag):
        self.db_cursor.execute(f"DELETE FROM tags where id={id} and name='{tag}'")

    @exception
    def showGuilds(self):
        self.db_cursor.execute('SELECT distinct * FROM guilds')
        return self.db_cursor.fetchall()

    @exception
    def showBans(self):
        self.db_cursor.execute('SELECT distinct * FROM bans')
        return self.db_cursor.fetchall()

    @exception
    def showHashTags(self):
        self.db_cursor.execute('SELECT distinct * FROM tags')
        return self.db_cursor.fetchall()