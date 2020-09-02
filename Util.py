import discord
import Constant

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