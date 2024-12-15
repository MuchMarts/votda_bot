import discord
from discord.ext import commands
from secret import TOKEN
import random
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is ready and running!")

@bot.commands()
async def roll(ctx, cmd: str, modifier: int):
    times = 1
    if cmd.index('d') != 0:
        try:
            times = cmd[:cmd.index('d')]
        except:
            print(f"Error: {cmd}")
    dice = 0

    try:
        dice = int(cmd[cmd.index('d')+1:])
    except:
        print(f"Error: {cmd}")

    rolls = []

    for i in range(times):
        rolls.append(random.randint(1, dice))

    sum = 0

    for roll in rolls:
        sum += roll

    msg = f"{times}d{dice} + {modifier} \n"
    msg += f"{rolls} = {roll} + {modifier}"

    await ctx.send(msg)
    
bot.run(TOKEN)