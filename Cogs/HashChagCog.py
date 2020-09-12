from discord.ext import commands
from Util import *
from Databases.Sqlite3 import *
from Databases.HerokuDB import *
import discord
import Constant


class HashChagCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def me(self, ctx):
        await ctx.send('me表示')

    @commands.group()
    async def hshg(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("サブコマンドがない->一覧出してあげよう")

    @hshg.command()
    async def add(self, ctx, tag):
        category = getHashChagCategory(ctx.guild.categories)

        for channel in category.channels:
            if tag.lower() == channel.name.lower():
                await ctx.send("もうタグは登録してあるにゃ～")
                return

        connectdb().addTag(int(ctx.guild.id), tag.lower())
        await ctx.guild.create_text_channel(name=tag, category=category)

    @hshg.command()
    async def delete(self, ctx, tag):
        category = getHashChagCategory(ctx.guild.categories)

        for channel in category.channels:
            if tag.lower() == channel.name.lower():
                connectdb().deleteTag(int(ctx.guild.id), tag.lower())
                await channel.delete()
                return

        await ctx.send("その名前のタグはないにゃ～")

    @hshg.command()
    async def show(self, ctx):
        tags = connectdb().showTags()
        await ctx.send(changeTagListToStr(tags))

    @hshg.command()
    async def shows(self, ctx):
        print(connectdb().showHashTags())
        print(connectdb().showGuilds())
        print(connectdb().showBans())
        await ctx.send("hoi")

    @hshg.command()
    async def ban(self, ctx, id):
        connectdb().addBan(ctx.guild.id, id)
        await ctx.send(f"{id}をBan登録したにゃ～")

    @hshg.command()
    async def unban(self, ctx, id):
        connectdb().deleteBan(ctx.guild.id, id)
        await ctx.send(f"{id}をBan解除したにゃ～")

    # TODO IDでしかみれないし...いる?サーバ名もBAN時に登録するようにするかどっちかやなぁ...
    @hshg.command()
    async def showban(self, ctx, id):
        await ctx.send("ハッシュタグ一覧")


def setup(bot):
    bot.add_cog(HashChagCog(bot))
