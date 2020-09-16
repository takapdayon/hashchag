import discord
import Constant
from Databases.Sqlite3 import *

def connectdb():
    if True:
        return Sqlite3()
    else:
        return Heroku()

def changeTagListToStr(taglist):
    str_tags = ""

    # forで回さずにjoinとかでできるならそっちに～
    for tag in taglist:
        str_tags += str(*tag) + "\n"

    return str_tags

def getHashChagCategory(categories):
    for category in categories:
        if category.name == Constant.APP_NAME:
            return category
    return None