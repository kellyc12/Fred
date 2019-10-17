import discord
from discord.ext import commands, tasks


# Set up Karma dictionary
karma = {}


class Karma(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Add points
    @commands.command(name='add',
                      description="Adds points to a user.")
    async def addpoints(self, ctx, num: int, member: discord.Member):

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
    async def info_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Sorry, I could not do that you are missing one or more arguments...')

    # Subtract points to Karma
    @commands.command(name='sub',
                        description="Subtracts points from a user.")
    async def subpoints(self, ctx, num: int, member: discord.Member):
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
    async def info_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Sorry, I could not do that you are missing one or more arguments...')

    @commands.command(name='ranking', description= "Returns a list of people ranked by most points.")
    async def display_rank(self, ctx):
        ranks = sorted(karma, key=karma.get, reverse=True)
        msg = "Here are the rankings: \n"
        num = 0
        for i in ranks:
            num = num + 1
            name = i
            points = karma[name]
            msg = msg + ("{0}. {1} - {2} \n".format(num, name, points))

        await ctx.send(msg)


def setup(client):
    client.add_cog(Karma(client))
