from discord.ext import commands
from Util import *
import traceback
import Constant
import Settings
import discord

TOKEN = Settings.TOKEN
INITIAL_EXTENSIONS = [
    'Cogs.HashChagCog'
]

class Main(commands.Bot):

    def __init__(self, command_prefix):
        super().__init__(command_prefix)

        for cog in INITIAL_EXTENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        print('-----')
        print(self.user.name)
        print(self.user.id)
        print('-----')

    async def on_guild_join(self, guild):
        print(type(guild))
        await guild.create_category(name=Constant.APP_NAME)
        #if (True):
        #   await guild.create_category(name="HashChag")

    async def on_guild_remove(self, guild):
        print("category削除")
        await guild.create_category(name=Constant.APP_NAME)

if __name__ == '__main__':
    bot = Main(command_prefix='#!')
    bot.run(TOKEN)