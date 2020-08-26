from discord.ext import commands
import traceback
import Settings

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

if __name__ == '__main__':
    bot = Main(command_prefix='!')
    bot.run(TOKEN)