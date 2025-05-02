from twitchio.ext import commands
import os
import requests

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=os.environ['TMI_TOKEN'],
            prefix='!',
            initial_channels=[os.environ['CHANNEL']]
        )

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        if message.echo:
            return

        print(f"{message.author.name}: {message.content}")

        requests.post("http://host.docker.internal:8084/input", json={"command": "a"})

        await self.handle_commands(message)

    @commands.command(name='hello')
    async def my_command(self, ctx):
        await ctx.send(f'Hello @{ctx.author.name}!')

if __name__ == "__main__":
    bot = Bot()
    bot.run()

