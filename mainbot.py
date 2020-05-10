import discord
import os
from discord.ext import commands
import ImportantContent


client = commands.Bot(command_prefix='!', case_insensitive=True)


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

@client.command()
async def off(ctx):
    print("Bot Off")
    await ctx.send("Shutting down... its getting so dark...")
    await client.logout()


# Say Hello
@client.command(name= 'hello')
async def helloworld(ctx):
    await ctx.send('Hello all {0.channel.mention}!'.format(ctx))


@client.command(name= "fred", description= 'A little summary of function.')
# TODO: Fix the formatting.
async def fred_intro(ctx):
    msg = 'Hello {0.author.mention}! How are you? I am here to tell you a little bit about myself! \n\n' \
          '\tYou can find out about my available commands by typing !help and also !help [specific command] will give you the details about that specific command \n\n' \
          'Latest updates: \n\n' \
          '\t - You can now use !timer to set the timer at any point and it will ping at next eot (:50). If you want a specific ping time it can be set by !timer [minute] \n' \
          '\t - Phrases will now save if the bot turns off and re-read them back after the bot turns back on.\n'\
          '\t - Did someone say memes? Coming up next is the jokes module for Fred! \n\n' \
          '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t Best,\n'\
          '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t Fred'
    await ctx.send(msg.format(ctx))


client.run(ImportantContent.token)
