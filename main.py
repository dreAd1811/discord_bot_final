
from asyncio.tasks import wait_for
import discord

import os
from discord import colour
from discord import client
from discord import user
from discord import embeds
from discord.embeds import Embed
import random
import aiohttp
import aiofiles
import asyncio
from discord_components.dpy_overrides import send
import praw
import giphy_client
from giphy_client.rest import ApiException
import json
import DiscordUtils
from random import choice
from asyncio import TimeoutError
from discord_components import *
import requests
from discord_buttons_plugin import *
import DiscordUtils
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice
import youtube_dl
import ffmpeg

import datetime

from dotenv import load_dotenv


from discord.ext import commands
from praw.reddit import Subreddit



DISCORD_TOKEN = ("DISCORD_TOKEN")


def get_prefix(client, message):
    with open('prefixes.json' , 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]




client = commands.Bot(command_prefix=get_prefix , help_command=None )
buttons = ButtonsClient(client) 


@client.event
async def on_ready():
	print("Bot Is Ready")

@client.event
async def on_guild_join(guild):
    with open('prefixes.json' , 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '.'

    with open('prefixes.json' , 'w') as f:
        json.dump(prefixes,f , indent=4)

@client.event
async def on_guild_remove(guild):
     with open('prefixes.json' , 'r') as f:
        prefixes = json.load(f)
        
        prefixes.pop(str(guild.id))
        with open('prefixes.json' , 'w') as f:
            json.dump(prefixes,f , indent=4)

@client.command()
async def changeprefix(ctx,prefix):
    with open('prefixes.json' , 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json' , 'w') as f:
        json.dump(prefixes,f , indent=4)

        await ctx.send(f'Prefix Sucessfully Changed to "{prefix}"! ✅')

@commands.has_any_role('Admin', 'Administrator', 'Mod', 'Moderator')
@client.command(name="slowmode" , description="Set Slow Mode To the Channel")
async def setdelay(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")


@commands.has_any_role('Admin', 'Administrator', 'Mod', 'Moderator')
@client.command(name="mute",description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="muted", description=f"{member.mention} was muted ", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" you have been muted from: {guild.name} reason: {reason}")

@client.command(name="unmute",description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   await member.send(f" you have unmutedd from: - {ctx.guild.name}")
   embed = discord.Embed(title="unmute", description=f" unmuted-{member.mention}",colour=discord.Colour.light_gray())
   await ctx.send(embed=embed)




@commands.has_any_role('Admin', 'Administrator', 'Mod', 'Moderator')
@client.command(pass_context = True)
async def kick(ctx, userName: discord.User):
    await client.kick(userName)
    await ctx.send(f'Kicked{userName.mention} Successfully ')


@commands.has_any_role('Admin', 'Administrator', 'Mod', 'Moderator')
@client.command(name='ban' , help='Bans A user Syntax: .ban @user')
async def ban(ctx , member : discord.Member,*,reason=None ):
	await member.ban(reason=reason)
	await ctx.send(f'Banned{member.mention} Successfully ')


@commands.has_any_role('Admin', 'Administrator', 'Mod', 'Moderator')
@client.command(name='unban' , help='Unbans A User Syntax = .unban name#1234')
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	
	member_name, member_discriminator = member.split('#')
	for ban_entry in banned_users:
		user = ban_entry.user
		
		if (user.name, user.discriminator) == (member_name, member_discriminator):
 			await ctx.guild.unban(user)
 			await ctx.channel.send(f"Unbanned: {user.mention} Successfully ")


@client.command(name='clear', help='this command will clear 100 messages In Channel')
async def clear(ctx, amount = 100):
    await ctx.channel.purge(limit=100)
    await ctx.send("Successfully Deleted 100 Messages ✔️ ") 

@client.command(name='deletechannel' , help='Deletes The Channel Syntax : .deletechannel <channelid>')
async def removechannel(ctx, channel_id: int):
    channel = client.get_channel(channel_id)
    await channel.delete()
    await ctx.send("Successfully deleted the channel ✔️ ")

@client.command(name='serverinfo' , help='Shows The Server Info')
async def server(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=name + " Server Information",
        description=description,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)

@client.command(name='dogimg' , help='Posts Random Dog Photos or Gifs')
async def dog(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/dog') # Make a request
      dogjson = await request.json() # Convert it to a JSON dictionary
   embed = discord.Embed(title="Doggo!", color=discord.Color.purple()) # Create embed
   embed.set_image(url=dogjson['link']) # Set the embed image to the value of the 'link' key
   await ctx.send(embed=embed) # Send the embed

@client.command()
async def userinfo(ctx):
    user = ctx.author

    embed=discord.Embed(title="USER INFO", description=f"Here is the info we retrieved about {user}", colour=user.colour)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="NAME", value=user.name, inline=True)
    embed.add_field(name="NICKNAME", value=user.nick, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="STATUS", value=user.status, inline=True)
    embed.add_field(name="TOP ROLE", value=user.top_role.name, inline=True)
    await ctx.send(embed=embed)


client.sniped_messages = {}


@client.event
async def on_message_delete(message):
    client.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

@client.command()
async def snipe(ctx):
    try:
        contents, author, channel_name, time = client.sniped_messages[ctx.guild.id]
        
    except:
        await ctx.channel.send("Couldn't find a message to snipe!")
        return

    embed = discord.Embed(description=contents, color=discord.Color.purple(), timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text=f"Deleted in : #{channel_name}")


    await ctx.channel.send(embed=embed)

    player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")

client.ticket_configs = {}

@client.event
async def on_ready():
    async with aiofiles.open("ticket_configs.txt", mode="a") as temp:
        pass

    async with aiofiles.open("ticket_configs.txt", mode="r") as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            client.ticket_configs[int(data[0])] = [int(data[1]), int(data[2]), int(data[3])]

    print(f"{client.user.name} is ready.")

@client.event
async def on_raw_reaction_add(payload):
    if payload.member.id != client.user.id and str(payload.emoji) == u"\U0001F3AB":
        msg_id, channel_id, category_id = client.ticket_configs[payload.guild_id]

        if payload.message_id == msg_id:
            guild = client.get_guild(payload.guild_id)

            for category in guild.categories:
                if category.id == category_id:
                    break

            channel = guild.get_channel(channel_id)

            ticket_channel = await category.create_text_channel(f"ticket-{payload.member.display_name}", topic=f"A ticket for {payload.member.display_name}.", permission_synced=True)
            
            await ticket_channel.set_permissions(payload.member, read_messages=True, send_messages=True)

            message = await channel.fetch_message(msg_id)
            await message.remove_reaction(payload.emoji, payload.member)

            await ticket_channel.send(f"{payload.member.mention} Thank you for creating a ticket! Use **'.close'** to close your ticket.")

            try:
                await client.wait_for("message", check=lambda m: m.channel == ticket_channel and m.author == payload.member and m.content == "-close", timeout=3600)

            except asyncio.TimeoutError:
                await ticket_channel.delete()

            else:
                await ticket_channel.delete()

@client.command()
async def configure_ticket(ctx, msg: discord.Message=None, category: discord.CategoryChannel=None):
    if msg is None or category is None:
        await ctx.channel.send("Failed to configure the ticket as an argument was not given or was invalid.")
        return

    client.ticket_configs[ctx.guild.id] = [msg.id, msg.channel.id, category.id] # this resets the configuration

    async with aiofiles.open("ticket_configs.txt", mode="r") as file:
        data = await file.readlines()

    async with aiofiles.open("ticket_configs.txt", mode="w") as file:
        await file.write(f"{ctx.guild.id} {msg.id} {msg.channel.id} {category.id}\n")

        for line in data:
            if int(line.split(" ")[0]) != ctx.guild.id:
                await file.write(line)
                
    await msg.add_reaction(u"\U0001F3AB")
    await ctx.channel.send("Succesfully configured the ticket system.")

@ client.command(pass_context=True , name="meme")
async def meme(ctx):
    embed = discord.Embed(title="", description="")
    async with aiohttp.ClientSession() as cs:
        async with cs.get(
            'https://www.reddit.com/r/memes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)


@client.command()
async def gif(ctx,*,q="random"):

    api_key="QQlCtxDa3asm3tdq0nSpwoGgDi0E17TC"
    api_instance = giphy_client.DefaultApi()

    try: 
    # Search Endpoint
        
        api_response = api_instance.gifs_search_get(api_key, q, limit=5, rating='g')
        lst = list(api_response.data)
        giff = random.choice(lst)

        emb = discord.Embed(title=q)
        emb.set_image(url = f'https://media.giphy.com/media/{giff.id}/giphy.gif')

        await ctx.channel.send(embed=emb)
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)

@client.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel : discord.TextChannel=None):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('Channel locked Successfully .')
@lock.error
async def lock_error(ctx, error):
    if isinstance(error,commands.CheckFailure):
        await ctx.send('You do not have permission to use this command!')

@client.command(name="invites")
async def invites(ctx, user = None):
  if user == None:
    totalInvites = 0
    for i in await ctx.guild.invites():
        if i.inviter == ctx.author:
            totalInvites += i.uses
    await ctx.send(f"You've invited {totalInvites} member{'' if totalInvites == 1 else 's'} to the server!")
  else:
    totalInvites = 0
    for i in await ctx.guild.invites():
       member = ctx.message.guild.get_member_named(user)
       if i.inviter == member:
         totalInvites += i.uses
    await ctx.send(f"{member} has invited {totalInvites} member{'' if totalInvites == 1 else 's'} to the server!")


@client.command(name="emojify" , description="Converts Text or Numbers Into Emojis!")
async def emojify(ctx,*,text):
    emojis = []
    for s in text.lower():
        if s.isdecimal():
            num2emo = {
                '0':'zero' , '1':'one' ,'2':'two' ,
                '3':'three' , '4':'four' ,'5':'five' ,
                '6':'six' , '7':'seven' ,'8':'eight' ,'9':'nine'}
            emojis.append(f':{num2emo.get(s)}:')
        elif s.isalpha():
            emojis.append(f':regional_indicator_{s}:')
        else:
            emojis.append(s)
    await ctx.send(' '.join(emojis))

@client.command(name="dogfact")
async def dogfact(ctx):
   async with aiohttp.ClientSession() as session:
      request2 = await session.get('https://some-random-api.ml/facts/dog')
      factjson = await request2.json()

   embed = discord.Embed(title="Dog Fact!", color=discord.Color.purple())
   embed.set_footer(text=factjson['fact'])
   await ctx.send(embed=embed)

@client.command(name="catfact")
async def dogfact(ctx):
   async with aiohttp.ClientSession() as session:
      request3 = await session.get('https://some-random-api.ml/facts/cat')
      factjson = await request3.json()

   embed = discord.Embed(title="Cat Fact!", color=discord.Color.purple())
   embed.set_footer(text=factjson['fact'])
   await ctx.send(embed=embed)

@client.command(name='catimg' , help='Posts Random Dog Photos or Gifs')
async def catimg(ctx):
   async with aiohttp.ClientSession() as session:
      request4 = await session.get('https://some-random-api.ml/img/cat') # Make a request
      dogjson = await request4.json() # Convert it to a JSON dictionary
   embed = discord.Embed(title="Cat!", color=discord.Color.purple()) # Create embed
   embed.set_image(url=dogjson['link']) # Set the embed image to the value of the 'link' key
   await ctx.send(embed=embed) # Send the embed

@client.command(name='joke' , help='Posts Random Joke')
async def dog(ctx):
   async with aiohttp.ClientSession() as session:
      request5 = await session.get('https://some-random-api.ml/joke') # Make a request
      dogjson = await request5.json() # Convert it to a JSON dictionary
   embed = discord.Embed(title="Joke!", color=discord.Color.purple()) # Create embed
   embed.set_footer(text=dogjson['joke']) # Set the embed image to the value of the 'link' key
   await ctx.send(embed=embed) # Send the embed

 
@client.command()
async def invite(ctx):
	embed = discord.Embed(title=f"Invite {client.user.name}", color=0xff0000, description=f"Wanna invite {client.user.name}, then [click here](https://discord.com/api/oauth2/authorize?client_id=876706121518317588&permissions=8&scope=bot)")
	await buttons.send(
		content = None,
		embed = embed,
		channel = ctx.channel.id,
		components = [
			ActionRow([
				Button(
					style = ButtonType().Link,
					label = "Invite",
					url = f"https://discord.com/api/oauth2/authorize?client_id=876706121518317588&permissions=8&scope=bot"
				)
			])
		]
	)


@client.command(name="helptesthello")
async def help(self,ctx):


    utility = discord.Embed(title="Utility Commands" , color=discord.Color.blue())
    utility.add_field(name="clear" , value="Deletes 100 Recent Messages \n syntax``.clear <amount>``")
    utility.add_field(name="snipe" , value="Shows the most Recent Deleted Message :face_with_hand_over_mouth: \n Syntax:``.snipe``")
    utility.add_field(name="deletechannel" , value="Deletes A channel . \n Syntax:``.removechannel <channelid>``")
    utility.add_field(name="userinfo" , value="Shows Information Of a User \n Syntax:``.userinfo @member``")
    utility.add_field(name="serverinfo" , value="Displays Info about the Server \n Syntax:``.serverinfo``")
    utility.add_field("Lock" , value="Locks a Channel ( Makes it READ ONLY to the members) \n Syntax:``.lock`` ( Use it in the channel u want to Lock)")
    utility.set_footer("Bot Made by dreadcreator#9999")

    moderation = discord.Embed(title="Moderation Commands" , color=discord.Color.red())
    moderation.add_field(name="Ban" , value=  "Bans A user")
    moderation.add_field(name="Unabn" , value= "Unbans A user")
    moderation.add_field(name="Kick" , value= "Kicks A user")
    moderation.add_field(name="Mute" , value= "Mutes A user")

    utility = discord.Embed(title="Utility Commands" , color=discord.Color.blue())
    utility.add_field(name="clear" , value="Deletes 100 Recent Messages \n syntax``.clear <amount>``")
    utility.add_field(name="snipe" , value="Shows the most Recent Deleted Message :face_with_hand_over_mouth: \n Syntax:``.snipe``")
    utility.add_field(name="deletechannel" , value="Deletes A channel . \n Syntax:``.removechannel <channelid>``")
    utility.add_field(name="userinfo" , value="Shows Information Of a User \n Syntax:``.userinfo @member``")
    utility.add_field(name="serverinfo" , value="Displays Info about the Server \n Syntax:``.serverinfo``")
    utility.add_field(name="Lock" , value="Locks a Channel ( Makes it READ ONLY to the members) \n Syntax:``.lock`` ( Use it in the channel u want to Lock)")

    funcmd = discord.Embed(title="Fun Commands!" , color=discord.Color.green())

    funcmd.add_field(name="meme" , value="Posts Random Meme . Dont Get Addicted to it  \n Syntax:``.meme``")
    funcmd.add_field(name="joke" , value="Posts Random Joke . U might Die Laughing! \n Syntax:``.joke``")
    funcmd.add_field(name="gif" , value="Posts Gif ( on Your Search) \n Syntax:``.gif search``")
    funcmd.add_field(name="catimg" , value="Sends Very Cute Cat Pictures awww! \n Syntax:``.catmig``")
    funcmd.add_field(name="catfact" , value="Posts Cat Facts That Will Amaze You. \n Syntax:``.catfact``")
    funcmd.add_field(name="dogimg" , value="Sends Random Dog Pictures  \n Syntax:``.dogimg``")
    funcmd.add_field(name="dogfact" , value="Posts Dog Facts That Will Amaze You. \n Syntax:``.dogfact``")
    funcmd.add_field(name="Emojify" , value="Converts Text or Numbers Into Emojis \n Syntax:``.emojify <text>``")




page1 = discord.Embed(title=" Moderation Commands", description="Help For You!", colour=discord.Colour.red())
page1.add_field(name="Ban" , value=  "Bans A user")
page1.add_field(name="Unabn" , value= "Unbans A user")
page1.add_field(name="Kick" , value= "Kicks A user")
page1.add_field(name="Mute" , value= "Mutes A user")

page2 = discord.Embed(title="Utility Commands", description="Help For You!", colour=discord.Colour.orange())
page2.add_field(name="clear" , value="Deletes 100 Recent Messages \n syntax``.clear <amount>``")
page2.add_field(name="snipe" , value="Shows the most Recent Deleted Message :face_with_hand_over_mouth: \n Syntax:``.snipe``")
page2.add_field(name="deletechannel" , value="Deletes A channel . \n Syntax:``.removechannel <channelid>``")
page2.add_field(name="userinfo" , value="Shows Information Of a User \n Syntax:``.userinfo @member``")
page2.add_field(name="serverinfo" , value="Displays Info about the Server \n Syntax:``.serverinfo``")
page2.add_field(name="Lock" , value="Locks a Channel ( Makes it READ ONLY to the members) \n Syntax:``.lock`` ( Use it in the channel u want to Lock)")
page2.add_field(name="setprefix" , value="Changes The prefix \n Syntax:``.setprefix <prefix>``")


page3 = discord.Embed(title="Fun Commands!", description="Help For You!", colour=discord.Colour.orange())
page3.add_field(name="meme" , value="Posts Random Meme . Dont Get Addicted to it  \n Syntax:``.meme``")
page3.add_field(name="joke" , value="Posts Random Joke . U might Die Laughing! \n Syntax:``.joke``")
page3.add_field(name="gif" , value="Posts Gif ( on Your Search) \n Syntax:``.gif search``")
page3.add_field(name="catimg" , value="Sends Very Cute Cat Pictures awww! \n Syntax:``.catmig``")
page3.add_field(name="catfact" , value="Posts Cat Facts That Will Amaze You. \n Syntax:``.catfact``")
page3.add_field(name="dogimg" , value="Sends Random Dog Pictures  \n Syntax:``.dogimg``")
page3.add_field(name="dogfact" , value="Posts Dog Facts That Will Amaze You. \n Syntax:``.dogfact``")
page3.add_field(name="Emojify" , value="Converts Text or Numbers Into Emojis \n Syntax:``.emojify <text>``")

client.help_pages = [page1, page2, page3]



@client.command()
async def help(ctx):
    buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"] # skip to start, left, right, skip to end
    current = 0
    msg = await ctx.send(embed=client.help_pages[current])
    
    for button in buttons:
        await msg.add_reaction(button)
        
    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

        except asyncio.TimeoutError:
            return print("test")

        else:
            previous_page = current
            if reaction.emoji == u"\u23EA":
                current = 0
                
            elif reaction.emoji == u"\u2B05":
                if current > 0:
                    current -= 1
                    
            elif reaction.emoji == u"\u27A1":
                if current < len(client.help_pages)-1:
                    current += 1

            elif reaction.emoji == u"\u23E9":
                current = len(client.help_pages)-1

            for button in buttons:
                await msg.remove_reaction(button, ctx.author)

            if current != previous_page:
                await msg.edit(embed=client.help_pages[current])

@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


@client.command(name="calcu")
async def cal(ctx):
   buttons = [
  [
    Button(style=ButtonStyle.grey, label='1'),
    Button(style=ButtonStyle.grey, label='2'),
    Button(style=ButtonStyle.grey, label='3'),
    Button(style=ButtonStyle.blue, label='×'),
    Button(style=ButtonStyle.red, label='EXIT'),
  ],

  [
    Button(style=ButtonStyle.grey, label='4'),
    Button(style=ButtonStyle.grey, label='5'),
    Button(style=ButtonStyle.grey, label='6'),
    Button(style=ButtonStyle.blue, label='÷'),
    Button(style=ButtonStyle.red, label='←'),
  ],

  [
    Button(style=ButtonStyle.grey, label='7'),
    Button(style=ButtonStyle.grey, label='8'),
    Button(style=ButtonStyle.grey, label='9'),
    Button(style=ButtonStyle.blue, label='+'),
    Button(style=ButtonStyle.red, label='CLEAR'),
  ],
  
  [
    Button(style=ButtonStyle.grey, label='00'),
    Button(style=ButtonStyle.grey, label='0'),
    Button(style=ButtonStyle.grey, label='.'),
    Button(style=ButtonStyle.blue, label='-'),
    Button(style=ButtonStyle.green, label='='),
  ],
]

def calculator(exp):
  o = exp.replace('x', '*')
  o = o.replace('÷', '/')
  result = ''
  try:
    result = str(eval(o))
  except:
    result='An error occurred'
  return result



client.run(DISCORD_TOKEN)
