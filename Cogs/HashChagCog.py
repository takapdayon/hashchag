from discord.ext import commands
from Util import *
from Databases.Sqlite3 import *
from Databases.HerokuDB import *
import discord
import Constant


class HashChagCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            connectdb().addGuild(int(guild.id), str(guild.name))
        except Exception as e:
            return

        category = getHashChagCategory(guild.categories)
        if category is not None:
            # TODO webHookを削除する
            [await channel.delete() for channel in category.channels]
            return

        await guild.create_category(name=Constant.APP_NAME)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        category = getHashChagCategory(guild.categories)
        connectdb().deleteGuild(guild.id)
        return

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel.category.name.lower() != Constant.APP_NAME.lower():
            return
        if message.content[:2] == "#!":
            return
        if message.guild.member_count > 5:
            return

        channels = self.bot.get_all_channels()
        await message.delete()

        # 発言サーバをBANしているサーバ取得
        banlist = connectdb().getBans(message.author.id)

        # webhook対象サーバ一覧を取得
        global_channels = [channel for channel in channels if channel.name == message.channel.name and \
                                                              str(channel.type) == "text" and \
                                                              channel.category.name.lower() == Constant.APP_NAME.lower()]

        for channel in global_channels:
            ch_webhooks = await channel.webhooks()
            webhook = discord.utils.get(ch_webhooks, name=message.channel.name)

            if webhook is None:
                continue
            await webhook.send(content=message.content,
                # サーバ表示にするかユーザ表示にするか悩む...一応サーバで表示します...
                # サーバとのつながりを意識したいから...
                username=f"{message.guild.name} {message.guild.id}",
                avatar_url=message.guild.icon_url_as(format="png"))
                #username=f"{message.author.name} {message.author.id}",
                #avatar_url=message.author.avatar_url_as(format="png"))

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
        tagl = tag.lower()

        if category is None:
            await ctx.send("hashchagカテゴリーがないにゃ～一回僕を追い出して再度入れてにゃ～")
            return

        for channel in category.channels:
            if tagl == channel.name.lower():
                await ctx.send(f"もう{tagl}は登録してあるにゃ～")
                return

        tag_channel = await ctx.guild.create_text_channel(name=tagl, category=category)
        await tag_channel.create_webhook(name=tagl)
        await ctx.send(f"タグ{tagl}を登録したにゃ～")

    @hshg.command()
    async def delete(self, ctx, tag):
        category = getHashChagCategory(ctx.guild.categories)
        tagl = tag.lower()

        for channel in category.channels:
            if tagl == channel.name.lower():
                await channel.delete()
                await ctx.send(f"タグ{tagl}を削除したにゃ～")
                return

        await ctx.send(f"{tagl}のタグはそもそもないにゃ～")

    @hshg.command()
    async def show(self, ctx):
        tags = ""

        channels = self.bot.get_all_channels()
        tag_channels = [channel for channel in channels if channel.category.name == Constant.APP_NAME.lower()]
        tag

        for channel in global_channels:
            tags += f"{channel.name}\n"

        await ctx.send(tags)

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
