import discord
from discord.ext import commands, tasks
import asyncio
from itertools import cycle
import ImportantContent
import random

status = cycle(['hello', 'twat', 'happy', 'sad'])

list = ['EOT WARNING! EOT WARNING! PING!', 'Maybe check the game... I dont care...', 'Blood for the blood god!!',
        'Build em up and knock em downn!', 'Mew Waz Ere', 'Here',
        'Here I am, brain the size of a planet... and you ask me to remind you about EOT.....',
        'Purple alert Purple alert!',
        'Call it extreme if you like, but I propose we hit it hard and hit it fast with a major - and I mean major - leaflet campaign.',
        'Howdily doodily do. I am Fred your chirpy BD companion.',
        'Don’t you think I’d love to be deceitful, unpleasant and offensive? Those are the human qualities I admire the most...',
        'I say they over there appear to be trying to kill us! Shall we have at them?',
        'Before this EOT, dont forget to do the right thing and turn missiles/nukes back on.']

random.shuffle(list)
phrases = cycle(list)

gid = ImportantContent.guild_id


class Time(commands.Cog):

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
        if (guild is not None) and (channel is not None) and (ping is not None):
            print("everything found")
            string = next(phrases) + ' {0.mention} {1.mention}'.format(ping, watcher)
            await channel.send(string)
        else:
            print("something is missing")



    # Start Command
    @commands.command(name='loop', description = "Starts a loop that changes the bot status")
    async def loop(self, ctx):
        await ctx.send("Loop beginning now!")

    # Start Command for timer
    @commands.command(name='timer', description = "Start the timer. Default time 60 min.")
    async def timer(self, ctx):
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
        list.append(string)
        global phrases
        random.shuffle(list)
        print(list)
        phrases = cycle(list)
        await ctx.send("Phrase added")

    @commands.command(name = 'showphrase', description = "Displays Fred's phrases.")
    async def show_phrase (self, ctx):
        text = ""
        for x in range(len(list)):
            line = str(x+1)+ ': ' + list[x] + '\n'
            text = text + line
        await ctx.send(text)

    @commands.command(name = "deletephrase", description = "Deletes a phrase from the list using the position of the phrase in the list")
    async def delete_phrase (self, ctx, index: int):
        text = list[index-1]
        list.remove(text)
        global phrases
        random.shuffle(list)
        phrases = cycle(list)
        await ctx.send('Removed phrase')

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        com = ctx.command
        if com == self.set_timer:
            self.timed_loop.start()

    # # trying something
    # @commands.command(name='timer')
    # async def timer(self, ctx, dur: int):
    #     while self.client
    #         print('switch on...')
    #         await asyncio.sleep(dur)
    #         await ctx.send("beep")


def setup(client):
    client.add_cog(Time(client))
