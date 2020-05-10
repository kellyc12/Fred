import discord
from discord.ext import commands, tasks
import asyncio
from itertools import cycle
import ImportantContent
import random
import datetime

status = cycle(['hello', 'twat', 'happy', 'sad'])

plist = []

random.shuffle(plist)
phrases = cycle(plist)

gid = ImportantContent.guild_id

#global to hold the minute for ping # default 50
remind_min = 50

# loop state set to
stateOfLoop = False

# helper function


def checktimer(min):
    tnow = datetime.datetime.now()
    tsett = tnow.replace(minute= min)
    diff = (tsett - tnow).total_seconds()/60
    if diff < 0:
        tsett = tsett.replace(hour = tsett.hour + 1)
        diff = (tsett - tnow).total_seconds()/60
    print ("this is the difference:", diff)
    return diff


def checkwithinloop(min):
    tnow = datetime.datetime.now()
    tsett = tnow.replace(hour = tnow.hour +1 , minute = min)
    diff = (tsett - tnow).total_seconds()/60
    print("This is the difference now:", diff)
    return diff

# helper function to write out the list or read in the list


def writeList ():
    outfile = open('/Users/kc97/PycharmProjects/DiscordBot/Fred/cogs/phrase', "w")
    for x in plist:
        outfile.write(x + '\n')
    outfile.close()
    return


def readList ():
    infile = open('/Users/kc97/PycharmProjects/DiscordBot/Fred/cogs/phrase', "r")
    lines = infile.readlines()
    if not (lines):
        infile.close()
        newfile = open('/Users/kc97/PycharmProjects/DiscordBot/Fred/cogs/phrase_backup', "r")
        lines = newfile.readlines()
        for line in lines:
            plist.append(line[:-1])
        newfile.close()
    else:
        for line in lines:
            plist.append(line[:-1])
        infile.close()
    return


class Timer(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Example of background tasks.
    @tasks.loop(seconds=10)
    async def statusloop(self):
        print('test phrase change')
        await self.client.change_presence(activity=discord.Game(next(phrases)))

    # trying my own
    @tasks.loop(minutes=60)
    async def timed_loop(self):
        guild = discord.Client.get_guild(self.client, ImportantContent.guild_id)
        channel = discord.Client.get_channel(self.client, ImportantContent.general_id)
        ping = discord.utils.get(guild.roles, name='Get Pinged')
        watcher = discord.utils.get(guild.roles, name='Watcher')
        global stateOfLoop
        # check time if the state is True
        if stateOfLoop:
            dur = checkwithinloop(remind_min)
            print("interval is", dur)
            self.timed_loop.change_interval(minutes=dur)

        if (guild is not None) and (channel is not None) and (ping is not None):
            print("everything found")
            # string = next(phrases) + ' {0.mention} {1.mention}'.format(ping, watcher)

            stateOfLoop = True
            await channel.send(next(phrases))
        else:
            print("something is missing")




    # Start Command
    @commands.command(name='loop', description = "Starts a loop that changes the bot status")
    async def loop(self, ctx):
        await ctx.send("Loop beginning now!")

    # Start Command for timer
    @commands.command(name='timer', description = "Start the timer. Default time 60 min.")
    async def timer(self, ctx, min = 50):
        global remind_min
        remind_min = min
        await ctx.send("Timer beginning now!")

    # Stop Command for timer
    @commands.command(name='t/o' , description = "Stop the timer. Time out.")
    async def timer_off(self, ctx):
        await ctx.send("Timer stopped!")

    # Invoke the loop with this event ^^
    @commands.Cog.listener()
    async def on_command(self, ctx):
        com = ctx.command
        print(com)
        if com == self.loop:
            self.statusloop.start()
        elif com == self.timer:
            dur = checktimer(remind_min)
            self.timed_loop.change_interval(minutes=dur)
            self.timed_loop.start()
        elif com == self.timer_off:
            self.timed_loop.cancel()
        else:
            return

    # Be added to the mentions list
    @commands.command(name='remind', description = "Add yourself to the timer's mention list.")
    async def remind_me(self, ctx):
        ping = discord.utils.get(ctx.guild.roles, name='Get Pinged')
        member = ctx.author
        await discord.Member.add_roles(member, ping)
        await ctx.send('{0.author.mention} added to the remind list'.format(ctx))

    # Be removed from the mentions list
    @commands.command(name='remove', description = "Remove yourself from the timer's mentions list.")
    async def remove_me(self, ctx):
        ping = discord.utils.get(ctx.guild.roles, name='Get Pinged')
        member = ctx.author
        await discord.Member.remove_roles(member, ping)
        await ctx.send('{0.author.mention} removed from the remind list'.format(ctx))

    # Command to change the loop duration
    @commands.command(name ='sett', description = 'Changes the timer duration.')
    async def set_timer(self, ctx, dur: int):
        self.timed_loop.cancel()
        self.timed_loop.change_interval(minutes= dur)
        await ctx.send("Time interval changed to {0} minutes".format(dur))

    # Command to add a phrase to Fred's list of phrases for EOT Warnings
    @commands.command(name ='addphrase', description = "Adds a phrase to Fred's list of phrases for EOT warnings.")
    async def add_phrase (self, ctx, string : str):
        plist.append(string)
        global phrases
        random.shuffle(plist)
        print(plist)
        phrases = cycle(plist)
        await ctx.send("Phrase added")

    @commands.command(name = 'showphrase', description = "Displays Fred's phrases.")
    async def show_phrase (self, ctx):
        text = ""
        for x in range(len(plist)):
            line = str(x+1)+ ': ' + plist[x] + '\n'
            text = text + line
        await ctx.send(text)

    @commands.command(name = "deletephrase", description = "Deletes a phrase from the list using the position of the phrase in the list")
    async def delete_phrase (self, ctx, index: int):
        text = plist[index-1]
        plist.remove(text)
        global phrases
        random.shuffle(plist)
        phrases = cycle(plist)
        await ctx.send('Removed phrase')

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        com = ctx.command
        if com == self.set_timer:
            self.timed_loop.start()

    # unload behavior?
    def cog_unload(self):
        writeList()
        print("cog unload behavior success")


def setup(client):
    readList()
    client.add_cog(Timer(client))



