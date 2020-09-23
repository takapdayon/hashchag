from discord.ext import commands
from Util import *
from Databases.Sqlite3 import *
from Databases.HerokuDB import *
import itertools
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
            [await channel.delete() for channel in category.channels]
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(manage_channels=False, mention_everyone=False, manage_webhooks=False),
            guild.me: discord.PermissionOverwrite(manage_channels=True, mention_everyone=True, manage_webhooks=True)
        }
        await guild.create_category(name=Constant.APP_NAME, overwrites=overwrites)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        category = getHashChagCategory(guild.categories)
        connectdb().deleteGuild(guild.id)
        return

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        ## DBに登録したID以外からの応答を拒否するようにする...?
        if message.channel.category.name.lower() != Constant.APP_NAME.lower():
            return
        ## TODO webhookがないならreturn
        if message.content.startswith("#!"):
            return
        if message.guild.member_count <= 5:
            await message.channel.send("鯖人数が5人未満だと使えないにゃ～")
            return

        channels = self.bot.get_all_channels()
        await message.delete()

        # 発言サーバをBANしているサーバ取得
        banlist = list(itertools.chain.from_iterable(connectdb().getbanList(message.guild.id)))

        # webhook対象サーバ一覧を取得
        global_channels = [channel for channel in channels if channel.name == message.channel.name and \
                                                              str(channel.type) == "text" and \
                                                              channel.category.name.lower() == Constant.APP_NAME.lower() and \
                                                              channel.guild.id not in banlist]

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

    @commands.group()
    async def hshg(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("サブコマンドを選択してにゃ～")

    @hshg.command()
    async def add(self, ctx, tag=None):
        category = getHashChagCategory(ctx.guild.categories)

        if category is None:
            await ctx.send("hashchagカテゴリーがないにゃ～一回僕を追い出して再度入れてにゃ～")
            return

        if tag is None:
            await ctx.send("追加タグ名がないにゃ～")
            return

        tagl = tag.lower()

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

        if category is None:
            await ctx.send("hashchagカテゴリーがないにゃ～一回僕を追い出して再度入れてにゃ～")
            return

        for channel in category.channels:
            if tagl == channel.name.lower():
                await channel.delete()
                await ctx.send(f"タグ{tagl}を削除したにゃ～")
                return

        await ctx.send(f"{tagl}のタグはそもそもないにゃ～")

    ## いづれ部分検索で引っ掛けて持ってこれるように
    @hshg.command()
    async def show(self, ctx):
        tags = ""

        channels = self.bot.get_all_channels()
        tag_channels = [channel.name for channel in channels if channel.category is not None and \
                                                          str(channel.type) == "text" and \
                                                          channel.category.name.lower() == Constant.APP_NAME.lower()]

        tag_channels = set(tag_channels)

        for channel in tag_channels:
            tags += f"{channel}\n"
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
    async def showban(self, ctx):
        name_and_banid = connectdb().getBans(ctx.guild.id)
        tags = ""

        if not name_and_banid:
            await ctx.send("ban鯖はないにゃ～")
            return

        for name, banid in name_and_banid:
            tags += f"{name} {banid}\n"
        await ctx.send(tags)

def setup(bot):
    bot.add_cog(HashChagCog(bot))
