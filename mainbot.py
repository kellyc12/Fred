import discord
import os
from discord.ext import commands
import ImportantContent

client = commands.Bot(command_prefix='!')


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


# Say Hello
@client.command(name= 'hello')
async def helloworld(ctx):
    await ctx.send('Hello all {0.channel.mention}!'.format(ctx))


client.run(ImportantContent.token)
