from discord.ext import commands
from Util import *
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
    async def add(self, ctx, tags):
        category = getHashChagCategory(ctx.guild.categories)

        for channel in category.channels:
            if tags == channel.name:
                await ctx.send("もうタグは登録してあるにゃ～")
                return
        # TODO DBにguild: tagsで登録する
        await ctx.guild.create_text_channel(name=tags, category=category)

    @hshg.command()
    async def delete(self, ctx):
        # TODO DBにguild: tagsを削除
        await ctx.send("ハッシュタグ削除")

    @hshg.command()
    async def show(self, ctx):
        await ctx.send("ハッシュタグ一覧")

    @hshg.command()
    async def gshow(self, ctx):
        await ctx.send("登録ハッシュタグ一覧")

    @hshg.command()
    async def ban(self, ctx, id):
        await ctx.send("ハッシュタグ一覧")


def setup(bot):
    bot.add_cog(HashChagCog(bot))
