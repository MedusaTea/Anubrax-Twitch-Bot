from twitchio.ext import commands
import os
import requests

path = 'http://host.docker.internal'

class Bot(commands.Bot):
    def sendInput(self, inputValue, hold):
        if hold:
            inputValue = "hold" + inputValue
        requests.post(path + ":8084/input", json={"command": inputValue})

    def loopInput(self, inputArray, hold):
        for char in list(inputArray):
            self.sendInput(char, hold)

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
    
        modCommandPrio = False
        if message.author.is_mod:
            match message.content:
                case "esc":
                    modCommandPrio = True
                    self.sendInput(message.content, False)


        holdIncluded = False
        if message.content.find('h') == 0:
            holdIncluded = True
            message.content = message.content.replace('hold', '')
            message.content = message.content.replace('h', '')
        
        if modCommandPrio == False:
            match message.content:
                case "a" | "s" | "d" | "e" | "c" | "x" | "f" | "z" | "q" | "l" | "p" | "j" | "l" | "o" | "m":
                    self.sendInput(message.content, False)
                case "left":
                    self.sendInput("a", False)
                case "click" | "lclick" | "leftclick":
                    self.sendInput("lclick", False)
                case "rclick" | "rightclick":
                    self.sendInput("rclick", False)
                case "right": 
                    self.sendInput("d", False)
                case "up": 
                    self.sendInput("w", False)
                case "down": 
                    self.sendInput("s", False)
                case "enter": 
                    self.sendInput("enter", False)
                case "space" | "jump":
                    self.sendInput("j", False)
                case "r" | "block":
                    self.sendInput("r", holdIncluded)
                case "walk" | "run" | "w":
                    self.sendInput("w", holdIncluded)
                case "map":
                    self.sendInput("m", False)
                case _:
                    self.loopInput(message.content, False)

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

