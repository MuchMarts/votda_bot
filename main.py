import discord
from discord.ext import commands
from secret import TOKEN
import random

from player import Player
from deck import Deck
from temp_db import strain_decks


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is ready and running!")

@bot.command()
async def roll(ctx, cmd: str, modifier: int = 0):
    times = 1
    if cmd.index('d') != 0:
        try:
            times = int(cmd[:cmd.index('d')])
        except:
            print(f"Error: {cmd}")
    dice = 0
    if times > 10000:
        await ctx.send("You can't roll more than 10000 times!")
        return
    
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
    msg += f"{rolls} = {sum} + {modifier} = {sum + modifier}"

    await ctx.send(msg)

players = []
active_deck = None

@bot.command()
async def create_game(ctx):
    global active_deck
    active_deck = Deck("Heartless", strain_decks["Heartless"])
    await ctx.send("Game created!")

@bot.command()
async def join_game(ctx):
    global players
    print(players)
    players.append(Player(ctx.author.name, ctx.author.id))
    await ctx.send(f"{ctx.author.name} has joined the game!")

@bot.group()
async def game(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Invalid command passed...")
    if ctx.author.id not in [player.id for player in players]:
        await ctx.send("You are not in the game!")

@game.command()
async def draw_card(ctx):
    global active_deck
    card = active_deck.draw_card()
    curr_player = [player for player in players if player.id == ctx.author.id][0]
    curr_player.add_strain_card(card)
    await ctx.send(f"{card.name}: {card.effect}")

@game.group(name="dnp")
async def draw_and_pick(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Invalid command passed...")

@draw_and_pick.command()
async def draw(ctx):
    global active_deck
    card = active_deck.draw_and_pick()
    drawn_cards = f"0. {card[0].name}: {card[0].effect}\n"
    drawn_cards += f"1. {card[1].name}: {card[1].effect}"
    await ctx.send(drawn_cards)

@draw_and_pick.command()
async def pick(ctx, choice: int):
    global active_deck
    if choice != 1 and choice != 2:
        await ctx.send("Invalid choice!")
        return
    card = active_deck.draw_and_pick(choice-1)
    curr_player = [player for player in players if player.id == ctx.author.id][0]
    curr_player.add_strain_card(card)
    await ctx.send(f"{card.name}: {card.effect}")

@game.command()
async def show_deck(ctx):
    global active_deck
    message = "Deck: \n"
    for card in active_deck.deck:
        message += f"{card.name}\n"
    await ctx.send(message)

@game.command()
async def show_ongoing(ctx):
    global active_deck
    message = "Ongoing Cards: \n"
    for i, card in enumerate(active_deck.ongoing_cards):
        message += f"{i}. {card.name}\n"
    await ctx.send(message)

@game.command()
async def reset_deck(ctx):
    global active_deck
    active_deck.reset_deck()
    await ctx.send("Deck has been reset!")

@game.command()
async def shuffle_deck(ctx):
    global active_deck
    active_deck.shuffle_deck()
    await ctx.send("Deck has been shuffled!")

@game.command()
async def remove_ongoing(ctx, index: int):
    global active_deck
    if index < 1 or index > len(active_deck.ongoing_cards):
        await ctx.send("Invalid index!")
        return
    card = active_deck.ongoing_cards.pop(index - 1)
    await ctx.send(f"{card.name} has been removed from ongoing cards!")

@game.command()
async def my_info(ctx):
    global players
    player = [player for player in players if player.id == ctx.author.id][0]
    message = f"{player.name} \n"
    message += f"Strain Taken: {player.strain_taken} \n"
    message += f"Strain Cards: \n"
    for card in player.strain_cards:
        message += f"{card.name}: {card.effect}\n Type: {card.type}\n"
    await ctx.send(message)

bot.run(TOKEN)