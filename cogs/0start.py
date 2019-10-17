import discord
from discord.ext import commands, tasks
import ImportantContent
import asyncio
from itertools import cycle


class Startup(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in as')
        print(self.client.user.name)
        print(self.client.user.id)
        print('------')


def setup(client):
    client.add_cog(Startup(client))
