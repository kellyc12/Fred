import discord
from discord.ext import commands, tasks
import ImportantContent
import asyncio
from itertools import cycle

BOT_PREFIX = "!"

bot = commands.Bot(command_prefix=BOT_PREFIX)
time = discord.Client()


# Set up Karma dictionary
karma = {}

status = cycle(['hello', 'twat', 'happy', 'sad'])

# Lets us know that Fred is running
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


# Add points to Karma
@bot.command(name='add',
             description="Add's Stars to a member's Star Chart")
async def addpoints(ctx, num: int, member: discord.Member):
    # Todo add something to check if username is valid

    user = member.display_name
    if user in karma:
        stars = karma.get(user)
        karma[user] = stars + num
        total = karma[user]
    else:
        karma[user] = num
        total = karma[user]
    await ctx.send("Added {0} points to {1.mention}! They now have {2} points :)".format(num, member, total))


@addpoints.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Sorry, I could not do that you are missing one or more arguments...')


# Subtract points to Karma
@bot.command(name='sub',
             description="Subtracts Stars to a member's Star Chart")
async def subpoints(ctx, num: int, member: discord.Member):
    # Todo add something to check if username is valid

    user = member.display_name
    if user in karma:
        stars = karma.get(user)
        karma[user] = stars - num
        total = karma[user]
    else:
        karma[user] = 0 - num
        total = karma[user]
    await ctx.send("Subtracted {0} points to {1.mention}! They now have {2} points :(".format(num, member, total))


@subpoints.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Sorry, I could not do that you are missing one or more arguments...')


@bot.command(name='ranking')
async def display_rank(ctx):
    ranks = sorted(karma, key=karma.get, reverse=True)
    msg = "Here are the rankings: \n"
    num = 0
    for i in ranks:
        num = num + 1
        name = i
        points = karma[name]
        msg = msg + ("{0}. {1} - {2} \n".format(num, name, points))

    await ctx.send(msg)

# Timer for EOT
# @tasks.loop(seconds=10)
# async def timer():
#     await ("EOT NOW!")

# Example of background tasks.
@tasks.loop(seconds=10)
async def statusloop():
    print('changing status')
    await bot.change_presence(activity=discord.Game(next(status)))



# Say Hello
@bot.command(name= 'hello')
async def helloworld(ctx):
    await ctx.send('Hello all {0.channel.mention}!'.format(ctx))


@bot.command(name = 'loop')
async def loop(ctx):
    await ctx.send("Loop beginning now!")

# Invoke the loop :O
@bot.event
async def on_command(ctx):
    com = ctx.command
    print(com)
    if com == loop:
        statusloop.start()
    else:
        return



bot.run(ImportantContent.token)
