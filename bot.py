from twitchio.ext import commands
import os
import requests

#path = 'http://172.18.64.1'
path = 'http://host.docker.internal'

class Bot(commands.Bot):
    def sendInput(self, inputValue):
        requests.post(path + ":8084/input", json={"command": inputValue})

    def loopInput(self, inputArray):
        self.sendInput(list(inputArray))

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
            case "a" | "w" | "s" | "d":
                self.sendInput(message.content)
            case "ctrl" | "click" | "atk" | "attack":
                self.sendInput("ctrl")
            case "up":
                self.sendInput("up")
            case "right": 
                self.sendInput("right")
            case "left":
                self.sendInput("left")
            case "down":
                self.sendInput("down")
            case "b" | "bomb":
                self.sendInput("b")
            case "i" | "item" | "space":
                self.sendInput("i")
            case "q" | "pill" | "card":
                self.sendInput("q")
            case "enter":
                self.sendInput("enter")
            case _:
                self.loopInput(message.content)

        await self.handle_commands(message)

    @commands.command(name='hello')
    async def my_command(self, ctx):
        await ctx.send(f'Hello @{ctx.author.name}!')

if __name__ == "__main__":
    bot = Bot()
    bot.run()

