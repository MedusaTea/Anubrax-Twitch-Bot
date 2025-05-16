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
            case "a" | "w" | "s" | "d" | "r" | "e" | "c" | "x" | "f" | "z" | "q":
                self.sendInput(message.content)
            case "ctrl" | "dash":
                self.sendInput("ctrl")
            case "lskill" | "ls":
                self.sendInput("q")
            case "rskill" | "rs":
                self.sendInput("e")
            case "cl":
                self.sendInput("z")
            case "cr":
                self.sendInput("c")
            case "right": 
                self.sendInput("d")
            case "left":
                self.sendInput("a")
            case "space" | "jump" | "j":
                self.sendInput("space")
            case "walk" | "shift" | "run" | "t":
                self.sendInput("toggleholdshift")
            case "map" | "tab" | "m":
                self.sendInput("tab")
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

