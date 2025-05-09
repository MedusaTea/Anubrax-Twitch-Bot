from twitchio.ext import commands
import os
import requests

#path = 'http://172.18.64.1'
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
            case "a" | "w" | "s" | "d":
                self.sendInput(message.content)
            case "ctrl" | "click":
                self.sendInput("ctrl")
            case "up" | "u":
                self.sendInput("up")
            case "right" | "r": 
                self.sendInput("right")
            case "left" | "l":
                self.sendInput("left")
            case "down" | "d":
                self.sendInput("down")
            case "b" | "bomb" | "e":
                self.sendInput("e")
            case "i" | "item" | "space":
                self.sendInput("space")
            case "q" | "pill" | "card":
                self.sendInput("q")
            case "holdfire" | "hf" | "stop" | "h" | "hold":
                self.sendInput("hold")
            case "enter":
                self.sendInput("enter")
            case "r":
                self.sendInput("r")
            case "f":
                self.sendInput("f")
            case _:
                self.loopInput(message.content)

        await self.handle_commands(message)

    @commands.command(name='hello')
    async def my_command(self, ctx):
        await ctx.send(f'Hello @{ctx.author.name}!')
    
    @commands.command(name='commands')
    async def my_command(self, ctx):
        await ctx.send(f'w,a,s,d - movments')
        await ctx.send(f'u,d,l,r - shoot directions')
        await ctx.send(f'i / item, b / bomb, q / pill')
        await ctx.send(f'enter, space')

if __name__ == "__main__":
    bot = Bot()
    bot.run()

