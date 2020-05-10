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
    msg = 'Hello {0.author.mention}! How are you? I am here to tell you a little bit about myself! \n' \
          'You can find out about my available commands by typing !help and also !help [specific command] will give you the details about that specific command \n' \
          '\n' \
          'Here is just a short run down of commands for your convenience: \n' \
          '     I.Karma type commands: \n' \
          '             -Add, sub, rankings. These commands help keep track of "Karma" points which is basically a fancy way of saying we praised you. \n' \
          '     II.Time type commands: \n' \
          '             -remind, remove, t/o, timer. These commands will allow you to enroll in the FredBot Eot reminders.' \
          '\n' \
          'Limitations: This bot will only be online when Laeyo is actively at a computer running the bot. If the bot shows as offline it will not function. \n' \
          '\n' \
          'If you have any questions or suggestions or functions you would like added please let me know! Happy to utilize my brain sometimes.' \
          '\n' \
          '\n' \
          'Best, \n' \
          '     Fred'
    await ctx.send(msg.format(ctx))


client.run(ImportantContent.token)
