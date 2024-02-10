# print("hello world")
import asyncio
import math
import nextcord
import random
from nextcord import Interaction
from nextcord.utils import get
from nextcord.ext import commands
from data import *
from random import randint
import array
intents = nextcord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)
XOMatch = False
input = 0
player1 = None
player2 = None


async def rotate_status():
    statuses = ['せーのっ', '触ったら逮捕！（Ah！）極Chu♡ de 点呼！（Uh！）', 'いちにーさんしー？（ごめんなさーい）']
    while True:
        for status in statuses:
            await client.change_presence(activity=nextcord.Game(name=status))
            await asyncio.sleep(3)


@client.event
async def on_ready():
    client.loop.create_task(rotate_status())
    # guild = client.get_guild(testServerId)
    print("Ready to go")
#     motivational_sentences = [
#     "Believe you can and you're halfway there.",
#     "The only way to do great work is to love what you do.",
#     "Don't watch the clock; do what it does. Keep going.",
#     "Success is not final, failure is not fatal: It is the courage to continue that counts.",
#     "You are never too old to set another goal or to dream a new dream.",
#     "The secret of getting ahead is getting started.",
#     "The future belongs to those who believe in the beauty of their dreams.",
#     "The harder you work for something, the greater you'll feel when you achieve it.",
#     "Don't be pushed around by the fears in your mind. Be led by the dreams in your heart.",
#     "Do not wait for opportunity. Create it.",
#     "The only limit to our realization of tomorrow will be our doubts of today."
# ]
#     saleh = guild.get_member(943872938967437372)
#     while True:
#         for sentence in motivational_sentences:
#             await saleh.send(sentence)
#             await asyncio.sleep(3)


testServerId = 317121657254707201
# 1148136613357043823
# 1148136614116216865


@client.slash_command(guild_ids=[testServerId])
async def say(ctx: Interaction, message: str):
    await ctx.response.send_message(message)

# @client.slash_command(guild_ids=[testServerId])
# async def say(ctx: Interaction, message: str):
# Welcome
# goodbye
# customize
# getter after setups
# ْXO
# send random
# gamble
# spy
# @client.slash_command(guild_ids=[testServerId])


@client.slash_command(guild_ids=[testServerId])
async def xo(ctx: Interaction, p2: nextcord.Member):

    board = {
        0: ":one:", 1: ":two:", 2: ":three:",
        3: ":four:", 4: ":five:", 5: ":six:",
        6: ":seven:", 7: ":eight:", 8: ":nine:"
    }
    channel = ctx.channel
    player1 = ctx.user
    player2 = p2
    x_moves = []
    o_moves = []
    await ctx.send(f"{player1.name} and {player2.name} are now playing.", ephemeral=True)
    await printboard(board, channel)
    await xohelper(channel, player1, player2, board, 0, x_moves, o_moves)


async def xohelper(channel: nextcord.TextChannel, p1: nextcord.Member, p2: nextcord.Member, board: dict, counter: int, x_moves: dict, o_moves: dict):

    await channel.send(f"It's {p1} turn")

    def validate_input(message):
        return message.author == p1 and message.channel == channel and message.content.isdigit() and 0 < int(
            message.content) < 10

    try:
        message = await client.wait_for("message", check=validate_input, timeout=30)
        move = int(message.content)
        if move not in x_moves and move not in o_moves:
            symbol = '❌' if counter % 2 == 0 else '⭕'
            board[move-1] = symbol
            x_moves.append(move) if symbol == '❌' else o_moves.append(move)
    except nextcord.errors.CommandError:
        await channel.send("You took too long to respond.")
        return

    await printboard(board, channel)

    if counter >= 4:
        if await checkwinner(x_moves, counter) or await checkwinner(o_moves, counter):
            await channel.send(f"{p1} has won")
            return

    if counter == 8 or await check_intersection(x_moves, o_moves):
        await channel.send("Draw")
        return

    await xohelper(channel, p2, p1, board, counter + 1, x_moves, o_moves)


async def printboard(board: dict, channel: nextcord.TextChannel):
    boardString = ""
    for i in range(0, len(board)):
        if i % 3 == 0:
            boardString += "\n"
        boardString += board.get(i, str(i))
    await channel.send(boardString)


async def checkwinner(moves, counter):
    winning_combinations = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9],
        [1, 5, 9],
        [3, 5, 7]
    ]
    for combination in winning_combinations:
        if all(move in moves for move in combination):
            return True
    return False


async def check_intersection(XArray, OArray):
    winning_combinations = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9],
        [1, 5, 9],
        [3, 5, 7]
    ]

    for combination in winning_combinations:
        intersects_X = any(cell in XArray for cell in combination)
        intersects_O = any(cell in OArray for cell in combination)
        # print("intersects_X: ", intersects_X, "intersects_O: ", intersects_X)
        if not (intersects_X and intersects_O):
            return False
    return True


@client.slash_command(guild_ids=[testServerId])
async def avatar(ctx: Interaction, member: nextcord.Member = None):
    if not member:
        member = ctx.user
    embed = nextcord.Embed(title=member).set_image(url=member.avatar.url)
    await ctx.response.send_message(embed=embed)


@client.slash_command(guild_ids=[testServerId])
async def dm(ctx: Interaction, victim: nextcord.Member, message: str):
    try:
        await victim.send(message)
        await ctx.send(f"DM sent to {victim.name}!", ephemeral=True)
    except Exception as e:
        await ctx.send("Message was not sent", ephemeral=True)

forbiddenWords = []


@client.slash_command(guild_ids=[testServerId])
async def ban(ctx: Interaction, message: str):
    forbiddenWords.append(message)
    await ctx.response.send_message(message+" Has been banned")


@client.slash_command(guild_ids=[testServerId])
async def rate(ctx: Interaction, member: nextcord.Member):
    random.seed(member.id)
    ratings = [
        f"{member.mention} is at most {random.randint(0, 10)} out of 10",
        f"I would rate {member.mention} a solid {random.randint(0, 10)} out of 10",
        f"{member.mention} deserves a {random.randint(0, 10)} out of 10 rating",
        f"For {member.mention}, I'd give a {random.randint(0, 10)} out of 10",
        f"{member.mention} is definitely {random.randint(0, 10)} out of 10"
    ]
    await ctx.send(random.choice(ratings))


@client.event
async def on_member_join(member: nextcord.Member):
    role = nextcord.utils.get(member.guild.roles, name='common')
    channel = client.get_channel(welcomeChannel)
    embed = nextcord.Embed(title=f'Welcome, {member.name}', description=f'Hi {member.mention}, we are glad to have you', color=0x0bf9f9).set_image(
        url=member.avatar.url)
    await member.add_roles(role)
    await channel.send(embed=embed)


@client.slash_command(guild_ids=[testServerId])
async def minesweeper(ctx: Interaction, size:int = 6):  # ADD default paramenets
    buttons = {
        -1: " ||:bomb: ||",
        0: "||:zero:||", 1: "||:one:||", 2: "||:two:||",
        3: "||:three:||", 4: "||:four:||", 5: "||:five:||",
        6: "||:six:||", 7: "||:seven:||", 8: "||:eight:||"
    }
    board = [0] * size**2
    # Select 10 unique random indices to replace with -1
    bombs = random.sample(range(len(board)), size+1)
    # Replace selected indices with -1
    for index in bombs:
        board[index] = -1

    for index in range(len(board)):
        if board[index] == -1:
            if index < size: # Check if its top
                #print("Top element")
                #Downward
                if board[index+size] != -1:
                    board[index+size] += 1
                if index % size - 1 != 0: # Top Right
                    #Left
                    if board[index-1] != -1:
                        board[index-1] += 1
                    #Downward Left
                    if board[index-1+size] != -1:
                        board[index-1+size] += 1

                elif index % size == 0: # Top Left
                    #Right
                    if board[index+1] != -1:
                        board[index+1] += 1
                    #Downward right
                    if board[index+1+size] != -1:
                        board[index+1+size] += 1
                
            elif (index + size >= 24): # Check if its bottom
                #print("Bottom Element")
                #Upward
                if board[index-size] != -1:
                    board[index-size] += 1
                if index % size - 1 != 0: # Bottom Right
                    #Left
                    if board[index-1] != -1:
                        board[index-1] += 1
                    #Upward Left
                    if board[index-1-size] != -1:
                        board[index-1-size] += 1

                elif index % size == 0: # Bottom Left
                    #Right
                    if board[index+1] != -1:
                        board[index+1] += 1
                    #Upward right
                    if board[index+1-size] != -1:
                        board[index+1-size] += 1
            else:
                #print("middle")
                #Downward
                if board[index+size] != -1:
                    board[index+size] += 1  
                #Left
                    if board[index-1] != -1:
                        board[index-1] += 1
                #Right
                    if board[index+1] != -1:
                        board[index+1] += 1
                #Upward
                if board[index-size] != -1:
                    board[index-size] += 1
                #Upward right
                if board[index+1-size] != -1:
                        board[index+1-size] += 1
                #Upward Left
                if board[index-1-size] != -1:
                        board[index-1-size] += 1
                #Downward right
                if board[index+1+size] != -1:
                        board[index+1+size] += 1
                #Downward Left
                if board[index-1+size] != -1:
                        board[index-1+size] += 1

    boardString = ""
    for i in range(0, len(board)):
        if i % size == 0:
            boardString += "\n"
        #boardString += " " + str(board[i])
        boardString += buttons.get(board[i], str(i))
    await ctx.channel.send(boardString)





# async def checkBomb(element, array):
#     size = math.sqrt(len(array))

#     if (element - 1 % size != 0) and (element + 1 % size !=0 ) and (element > size) and (element + size > len(array)):
#         checklist = [array[]]

#     if element - 1 % size == 0:  # Element in the left side
#         print("|")  # Check the exact right
#         if element > size:  # Element isnt on Top
#             print("")  # Check the top
#         if element + size < len(array):  # Element isnt inthe bottom
#             print("") #check the bottom and its right
#         # Check the 
#     elif element + 1 % size == 0:  # Element in the right side
#         print("Right")
#     # if element < size: # Element in the Top
#     #    print("")
#     if element + size > len(array):  # Element in the bottom
#         print("")


@client.event
async def on_member_remove(member: nextcord.Member):
    channel = client.get_channel(welcomeChannel)
    embed = nextcord.Embed(title=f'Goodbye, {member.name}', description="you will be mist", color=0x0bf9f9).set_image(
        url=member.avatar.url)
    await channel.send(embed=embed)


@client.event
async def on_message(message):
    role = nextcord.utils.get(message.guild.roles, name='Slave')
    if message.content in forbiddenWords:
        await message.channel.send("لاعاد تعودها")
        await message.delete()
    if isinstance(message.author, nextcord.Member) and role in message.author.roles:
        await message.delete()
        await message.channel.send("سد حلقك")

# role with reactions ***

client.run(APIKey)
