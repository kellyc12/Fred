import discord
from discord.ext import commands, tasks
import asyncio
from itertools import cycle

status = cycle(['hello', 'twat', 'happy', 'sad'])



class Time(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Example of background tasks.
    @tasks.loop(seconds=10)
    async def statusloop(self):
        print('changing status')
        await self.client.change_presence(activity=discord.Game(next(status)))

    # Start Command
    @commands.command(name='loop')
    async def loop(self, ctx):
        await ctx.send("Loop beginning now!")

    # Invoke the loop with this event ^^
    @commands.Cog.listener()
    async def on_command(self, ctx):
        com = ctx.command
        print(com)
        if com == self.loop:
            self.statusloop.start()
        else:
            return


def setup(client):
    client.add_cog(Time(client))
