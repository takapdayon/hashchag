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

def deleteCategory():
    print("カテゴリ削除")

def deleteCannel():
    print("チャンネル削除")

def createCannel():
    print("チャンネル作成")

def checkHashTag():
    print("すでにそのハッシュタグがあるか")

def addHashTag():
    print("ハッシュタグ登録")

def addGlobalHashTag():
    print("全体のハッシュタグとして登録")

def showHashTags():
    print("登録されているハッシュタグ一覧")

def showGlobalHashTags():
    print("ハッシュタグ一覧")

def checkparent():
    print("親カテゴリーがhashchagかどうか")

def getHashChagCategory(categories):
    for category in categories:
        if category.name == Constant.APP_NAME:
            return category
    return None