from twitchio.ext import commands
import os
import httpx
import asyncio

path = 'http://host.docker.internal'

CHATTERS_FILE = 'chatters.txt'

def load_chatters():
    try:
        with open(CHATTERS_FILE, 'r') as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return set()

def save_chatter(username):
    with open(CHATTERS_FILE, 'a') as f:
        f.write(f"{username}\n")

class Bot(commands.Bot):
    aHolding = False
    dHolding = False
    rHolding = False

    def __init__(self):
        super().__init__(
            token=os.environ['TMI_TOKEN'],
            prefix='!',
            initial_channels=[os.environ['CHANNEL']]
        )
        self.known_chatters = load_chatters()
        self.client = httpx.AsyncClient()

    async def sendInput(self, inputValue, hold):
        if hold:
            inputValue = "hold" + inputValue
        response = await self.client.post(path + ":8084/input", json={"command": inputValue})
        response.raise_for_status()

    async def loopInput(self, inputArray, hold):
        for char in list(inputArray):
            match char:
                case "y":
                    await self.sendInput("enter", hold)
                case "a":
                    if self.dHolding:
                        await self.sendInput("d", False)
                        self.dHolding = False
                    self.aHolding = holdIncluded
                    await self.sendInput(char, holdIncluded)
                case "d":
                    if self.aHolding:
                        await self.sendInput("a", False)
                        self.aHolding = False
                    self.dHolding = holdIncluded
                    await self.sendInput(char, holdIncluded)
                case "w" | "s" | "e" | "c" | "x" | "f" | "z" | "q" | "l" | "p" | "j" | "l" | "o":
                    await self.sendInput(char, False)

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')

    async def clear_holds(self):
        if self.dHolding:
            await self.sendInput("d", False)
            self.dHolding = False
        
        if self.aHolding:
            await self.sendInput("a", False)
            self.aHolding = False
        
        if self.rHolding:
            await self.sendInput("r", False)
            self.rHolding = False

    async def event_message(self, message):
        if message.echo:
            return

        if message.author.name not in self.known_chatters:
            await message.channel.send(f'Welcome @{message.author.name}! :)')
            self.known_chatters.add(message.author.name)
            save_chatter(message.author.name)

        print(f"{message.author.name}: {message.content}")
    
        modCommandPrio = False
        if message.author.is_mod:
            match message.content:
                case "esc":
                    await self.clear_holds()
                    modCommandPrio = True
                    await self.sendInput(message.content, False)


        holdIncluded = False
        if message.content.find('h') == 0:
            holdIncluded = True
            message.content = message.content.replace('hold', '')
            message.content = message.content.replace('h', '')
        
        if modCommandPrio == False and len(message.content.split()) == 1:
            match message.content:
                case "a":
                    if self.dHolding:
                        await self.sendInput("d", False)
                        self.dHolding = False
                    self.aHolding = holdIncluded
                    await self.sendInput(message.content, holdIncluded)
                case "d":
                    if self.aHolding:
                        await self.sendInput("a", False)
                        self.aHolding = False
                    self.dHolding = holdIncluded
                    await self.sendInput(message.content, holdIncluded)
                case "w" | "s" | "e" | "c" | "x" | "f" | "z" | "q" | "l" | "p" | "j" | "l" | "o":
                    await self.sendInput(message.content, False)
                case "tab":
                    await self.clear_holds()
                    await self.sendInput("tab", False)
                case "left":
                    await self.sendInput("a", False)
                case "click" | "lclick" | "leftclick":
                    await self.sendInput("lclick", False)
                case "rclick" | "rightclick":
                    await self.sendInput("rclick", False)
                case "right": 
                    await self.sendInput("d", False)
                case "up": 
                    await self.sendInput("w", False)
                case "down": 
                    await self.sendInput("s", False)
                case "enter" | "y": 
                    await self.clear_holds()
                    await self.sendInput("enter", False)
                case "space" | "jump":
                    await self.sendInput("j", False)
                case "r" | "block":
                    self.rHolding = holdIncluded
                    await self.sendInput("r", holdIncluded)
                #case "walk" | "run" | "w":
                    #self.sendInput("w", holdIncluded)
                case "map":
                    await self.sendInput("m", False)
                case _:
                    await self.loopInput(message.content, False)

        await self.handle_commands(message)

    @commands.command(name='hello')
    async def my_command(self, ctx):
        await ctx.send(f'Hello @{ctx.author.name}!')
    
    @commands.command(name='commands')
    async def my_command(self, ctx):
        await ctx.send(f'on overlay only today')

    async def close(self):
        await self.client.aclose()

if __name__ == "__main__":
    bot = Bot()
    try:
        bot.run()
    finally:
        asyncio.run(bot.close())
