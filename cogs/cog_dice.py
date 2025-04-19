import discord
from discord.ext import commands
import random

class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def roll(self, ctx):
        pass

    @commands.command()
    async def flip(self, ctx, times:int=1):
        
        if times < 1:
            return
        
        output = "(" + times + ") Results: "

        for i in range(times):
            if(random.randint(0, 1) == 0):
                output += "Heads "
            else:
                output += "Tails "

        await ctx.send(output)
