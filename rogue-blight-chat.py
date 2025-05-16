from twitchio.ext import commands
import os
import requests

path = 'http://host.docker.internal'

class Bot(commands.Bot):
    def sendInput(self, inputValue):
        requests.post(path + ":8084/input", json={"command": inputValue})

    def loopInput(self, inputArray):
        for char in list(inputArray):
            self.sendInput(char)

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
        
        match message.content:
            case "a" | "s" | "d" | "r" | "e" | "c" | "x" | "f" | "z" | "q" | "l" | "p" | "j" | "l" | "o" | "m":
                self.sendInput(message.content)
            case "right": 
                self.sendInput("d")
            case "left":
                self.sendInput("a")
            case "space" | "jump":
                self.sendInput("j")
            case "walk" | "run" | "w":
                self.sendInput("togglew")
            case "map":
                self.sendInput("m")
            case _:
                self.loopInput(message.content)

        await self.handle_commands(message)

    @commands.command(name='hello')
    async def my_command(self, ctx):
        await ctx.send(f'Hello @{ctx.author.name}!')
    
    @commands.command(name='commands')
    async def my_command(self, ctx):
        await ctx.send(f'on screen only today')

if __name__ == "__main__":
    bot = Bot()
    bot.run()

