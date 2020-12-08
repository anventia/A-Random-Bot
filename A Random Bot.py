print('Importing Libraries...')
import discord
from discord.ext import commands
import random
from discord.ext.commands import has_permissions, CheckFailure
import asyncio
import datetime
import requests
import json
import math
import re
import num2words
from num2words import num2words
import os
import psutil
import riotwatcher
from riotwatcher import LolWatcher, ApiError

# Read + write functions
def read_file(filename):
    with open(filename, 'r') as f:
        load = json.load(f)
    return load

def write_file(dictionary, filename):
    with open(filename, 'w') as f:
        json.dump(dictionary, f, indent=4)

# Startup
print("Declaring Variables...")
r = " "
prefix = read_file("config.json")["prefix"]
bot_icon = "https://cdn.discordapp.com/avatars/521086131132039169/293d65f8ba1ca83c95f0dfb6a1fd240b.png?size=1024"
exclamation = "https://i.postimg.cc/52Ty19d9/exclamationpoint.png"
xmark = "https://i.postimg.cc/zDxJ8DTm/xmark.png"
checkmark = "https://i.postimg.cc/Njmq9Q2j/checkmark.png"
bsquare= "https://i.postimg.cc/nhxLdSJT/bsquare.png"
version = '1.8.2'
botname = "A Random Bot"
embedcolour = 0x6400FF
bot = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=discord.Intents.all())
bot.remove_command("help") #Removes default help command
bsquaremoji = "<:bsquare_round:731276725794635828>"
xmarkmoji = "<:xmark_round:732374828505497661>"
checkmarkmoji = "<:checkmark_round:732374828551634986>"
upvotemoji = "<:upvote_r:749455616128450642>"
downvotemoji = "<:downvote_r:749456269995278457>"

print("Starting up...")
@bot.event  # Startup
async def on_ready():
    await bot.change_presence(activity=discord.Activity(name="for commands | >help", type=discord.ActivityType.watching))
    print('Status Updated')
    print('Logged in as {0.user}'.format(bot))

@bot.command(name="debug")
async def debug(ctx, toggle="None"):
    if not str(ctx.author.id) == "327948165468782595":
        await senderror(ctx, "You are not allowed to use that!")
        return
    if toggle.capitalize() == "On":
        await sendcheck(ctx, "Debugging mode has been turned on.")
        await bot.change_presence(activity=discord.Activity(name="Debugging Mode, may be unstable", type=discord.ActivityType.playing))
    elif toggle.capitalize() == "Off":
        await sendcheck(ctx, "Debugging mode has been turned off.")
        await bot.change_presence(activity=discord.Activity(name="for commands | >help", type=discord.ActivityType.watching))
    else:
        await invalidargs(ctx)
        return

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

#async def on_message(message):
    #if message.author == "327948165468782595":
        #if message.startswith(">"):
            #print("test")
            #await message.channel.send("You are currently blocked from using the bot!")
            #return

@bot.command(aliases=["tst", "tes"])
async def test(ctx):
    await ctx.send("test")

@bot.command(name="fil") # File reading test
async def fil(ctx, line):
    test = open("test.txt", "r")
    a = test.read()
    list = a.split("\n")
    res= list[int(line)-1]
    await ctx.send(res)

# Functions
async def invalidargs(ctx):
    embed = discord.Embed(colour=embedcolour)
    embed.set_author(name="Error: Invalid Arguments.", icon_url=xmark)
    await ctx.send(embed=embed)

async def senderror(ctx, error):
    embed = discord.Embed(colour=embedcolour)
    embed.set_author(name=error, icon_url=xmark)
    await ctx.send(embed=embed)

async def sendcheck(ctx, text):
    embed = discord.Embed(colour=embedcolour)
    embed.set_author(name=text, icon_url=checkmark)
    await ctx.send(embed=embed)

async def sendsquare(ctx, text):
    embed = discord.Embed(colour=embedcolour)
    embed.set_author(name=text, icon_url=bsquare)
    await ctx.send(embed=embed)

async def checkPerms(user:discord.Member, perm):
    permvalue = user.permissions
    permissions = discord.Permissions(permissions=permvalue)
    return permissions


@bot.command(name="cptest")
async def cptest(ctx, user:discord.Member, perm):
    await ctx.send(checkPerms(user, perm))

# System
@bot.command(name="help")  # New help command
async def help(ctx, category = "None"):
    f = open("help.txt", "r")
    category = category.capitalize().strip()
    commandline = []
    helpList = {}
    header = 0
    v1 = "\u200b"
    title = ""
    tList = ""  # List of all the titles/categories
    for line in f:  # for each line... Scans to dict "helpList"
        if line.startswith("[["):  # Title
            title = line
            tList += line.replace("[[", "").replace("]]", "").replace("bottom", "")
            header = header + 1
        elif "---" in line:  # Divider between categories
            x = ""
            y = ""
            for i in commandline:
                split = i.split("|")   # Content of the command line, split into list
                if ">>>" in split[0]:  # Is line a newpage indicator?
                    x += ">>>\n"
                    y += ">>>\n"
                else:
                    x += split[0].strip() + "\n"  # Command name
                    y += split[1].strip() + "\n"  # Command description
            headernumber = "h{}".format(str(header))
            helpList[headernumber] = dict()
            helpList[headernumber]["title"] = title
            helpList[headernumber]["commands"] = x
            helpList[headernumber]["descriptions"] = y
            commandline = []
        else:  # Command line
            commandline.append(line)

    if category == "All":  # If user requests all categories
        embed = discord.Embed(colour=embedcolour)
        embed.set_author(name="Help page #0 for {}".format(botname), icon_url=bot_icon)
        embed.set_footer(text='() == argument not required.\nIf you have any ideas for commands or things to add to commands, tell @TheUntraceable#9430')
        user = ctx.author
        hcount = 1
        page = 1
        await sendsquare(ctx, "Sending help message(s) to your DMs!")
        for i in helpList:
            res_title = (helpList["h{}".format(hcount)]["title"]).replace("[[", "").replace("]]", "")
            x = helpList["h{}".format(hcount)]["commands"]
            y = helpList["h{}".format(hcount)]["descriptions"]
            hcount = hcount + 1

            if not ">>>" in x:
                embed.add_field(name=res_title, value=x, inline=True)
                embed.add_field(name=v1, value=v1, inline=True)
                embed.add_field(name=v1, value=y, inline=True)
            else:
                x = x.replace(">>>\n", "")
                y = y.replace(">>>\n", "")
                await user.send(embed=embed)
                embed = discord.Embed(colour=embedcolour)
                embed.set_author(name="Help page #{} for {}".format(str(page), botname), icon_url=bot_icon)
                embed.set_footer(text='() == argument not required.\nIf you have any ideas for commands or things to add to commands, tell @TheUntraceable#9430\ntest')
                embed.add_field(name=res_title, value=x, inline=True)
                embed.add_field(name="test", value=v1, inline=True)
                embed.add_field(name=v1, value=y, inline=True)
                page = page + 1
        await user.send(embed=embed)

    elif category == "None":  # If category is left blank
        embed = discord.Embed(colour=embedcolour)
        embed.set_author(name="Help page for help command", icon_url=bot_icon)
        embed.add_field(name="Categories:",value=tList)
        embed.add_field(name="Usage:", value=">help [category]")
        embed.set_footer(text="Do >info for support server if anything\nis not working or you need help.")
        await ctx.send(embed=embed)

    else:  # If user requests a specific category
        res_title = None
        for i in helpList:
            currenttitle = helpList[i]["title"].replace("[[", "").replace("]]", "").replace("\n", "")
            if currenttitle == category:  # If requested title is located
                res_title = currenttitle
                x = helpList[i]["commands"]
                y = helpList[i]["descriptions"]
        if res_title == None:
            await senderror(ctx, "Error: Category not found!")
            return
        x = x.replace(">>>", "")
        y = y.replace(">>>", "")
        embed = discord.Embed(colour=embedcolour)
        embed.set_author(name="Help command", icon_url=bot_icon)
        embed.set_footer(text='() == argument not required.\nIf you have any ideas for commands or things to add to commands, tell @TheUntraceable#9430')
        embed.add_field(name=res_title, value=x, inline=True)
        embed.add_field(name=v1, value=v1, inline=True)
        embed.add_field(name=v1, value=y, inline=True)
        await ctx.send(embed=embed)

@bot.command(name="commands")  # Shows all available commands, without descriptions, only basic info.
async def commands(ctx):
    embed = discord.Embed(colour=embedcolour)
    embed.set_author(name="Help command for {}".format(botname), icon_url=bot_icon)
    f = open("help.txt", "r")
    title = ""
    temp = []
    t = "0"
    line2 = ""
    user = ctx.author
    v1 = "\u200b"
    c1 = 1
    for line in f:
        if line.startswith("[["):
            title = line
        elif "---" in line:
            x = ""
            y = ""
            c = 1
            for i in temp:
                split = i.split("|")
                if c == 1:
                    x += "`{}` ".format(split[0])
                    c = 2
                else:
                    x += "`{}`\n".format(split[0])
                    c = 1
            title = title.replace("[[", "")
            title = title.replace("]]", "")
            if c1 == 1:
                embed.add_field(name=title, value=x, inline=True)
                c1 = 2
            else:
                embed.add_field(name=v1, value=v1, inline=True)
                embed.add_field(name=title, value=x, inline=True)

                c1 = 1
            temp = []
        else:
            if not ">>>" in line:
                temp.append(line)

    await ctx.send(embed=embed)

@bot.command(name='info')
async def info(ctx):
    v1 = '\u200b'
    v2 = '\u200b'
    v3 = '\u200b'
    global r
    r = len(open("A Random Bot.py", "r", encoding="cp850").read().split("\n"))
    guilds = len(bot.guilds)

    pid = os.getpid()
    py = psutil.Process(pid)
    memoryUse = py.memory_info()[0] / 2. ** 30


    embed = discord.Embed(colour=embedcolour)
    embed.set_author(name='{} Information Page'.format(botname), icon_url=bot_icon)

    embed.add_field(name='Info:', value='Created on:\nVersion:\nCurrent prefix:',inline=True)
    embed.add_field(name=v2, value=v3, inline=True)
    embed.add_field(name=v1, value='2020/04/22\n v{}\n`{}` (You should know that already...)'.format(version, prefix), inline=True)

    #embed.add_field(name='System:', value='Memory Usage:', inline=True)
    #embed.add_field(name=v2, value=v3, inline=True)
    #embed.add_field(name=v1,value=f'{memoryUse}',inline=True)

    embed.add_field(name='Credits:', value='Coding:\nAdditional code:\nIcons:\nCoded with:', inline=True)
    embed.add_field(name=v2, value=v3, inline=True)
    embed.add_field(name=v1, value='<@327948165468782595>\n<@417382632247001088>, <@506696814490288128>, and <@353004385334198272>\n<@327948165468782595>\nPython 3.9: discord.py', inline=True)

    embed.add_field(name='Other:', value='Support server:\nDiscord Bot List:', inline=True)
    embed.add_field(name=v2, value=v3, inline=True)
    embed.add_field(name=v1, value=f'https://discord.gg/CqANQvj\nhttps://top.gg/bot/521086131132039169', inline=True)

    embed.set_footer(text="{} lines of code, used in {} servers.".format(r, guilds))
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong! {0}ms".format(round(bot.latency*1000, 1)))

# Moderation
@bot.command(name="rr")
async def rr(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)


@has_permissions(manage_messages=True)  # Clear command
@bot.command(name="clear")
async def wipe(ctx, amount):
    #if ctx.message.author.id == 506696814490288128:
        #return

    if int(amount) > 0:
        await ctx.channel.purge(limit=int(amount)+1)
        now=datetime.datetime.now()
        log = "> CLEAR: {} || {} messages cleared by {} in channel '{}' in '{}'".format(now, amount, ctx.message.author, ctx.channel, ctx.guild.name)
        print(log)
        print(log, file=open('log.txt', 'a'))
    else:
        await senderror(ctx, "Error: Amount must be larger than zero!")

@wipe.error
async def wipe_error(ctx, error):
    if isinstance(error, CheckFailure):
        await senderror(ctx, "Error: You are missing the Manage Messages permission!")

@has_permissions(administrator=True)
@bot.command(aliases=["wchannel"])
async def warnchannel(ctx, chan = "None"):
    config = read_file("warnconfig.txt")
    server = str(ctx.guild.id)
    if server not in config:  # If server doesn't exist yet
        config[server] = dict()
    else:
        if chan == config[server]["channel"]:
            await senderror(ctx, "Error: That channel is already set!")
            return
    if chan == "None":
        if "channel" not in config[server]:
            currentchannel = "No warning channel has been set yet!"
        else:
            currentchannel = config[server]["channel"]
        embed = discord.Embed(colour=embedcolour, description=currentchannel)
        embed.set_author(name="Current warning channel:", icon_url=bsquare)
        await ctx.send(embed=embed)
        return
    if "channel" not in config[server]:  # If channel doesn't exist yet
        config[server]["channel"] = dict()
        oldchannel = "None"
    else:
        oldchannel = config[server]["channel"]
    config[server]["channel"] = chan
    if "name" not in config[server]:  # If channel doesn't exist yet
        config[server]["name"] = dict()
        config[server]["name"] = ctx.guild.name
    if any(c in chan for c in "<#>") and len(chan) == 21:
        pass
    else:
        #print("invalid channel")
        await senderror(ctx, "Error: Invalid Channel!")
        return

    embed=discord.Embed(colour=embedcolour, description=f"Old Channel: {oldchannel}\nNew Channel: {chan}")
    embed.set_author(name="Server Warning Channel has been updated.", icon_url=checkmark)
    await ctx.send(embed=embed)
    write_file(config, "warnconfig.txt")

@warnchannel.error
async def warnchannel_error(ctx, error):
    if isinstance(error, CheckFailure):
        embed = discord.Embed(colour=embedcolour)
        embed.set_author(name="You are missing the Administrator permission!", icon_url=xmark)
        await ctx.send(embed=embed)

@has_permissions(manage_messages=True)
@bot.command(name="warn")
async def warn(ctx, user: discord.Member = "None", *, reason = "None"):
    if user == "None" or str(reason) == "None":
        await invalidargs(ctx)
        return
    config = read_file("warnconfig.txt")
    server = str(ctx.guild.id)
    if server not in config:
        embed = discord.Embed(colour=embedcolour)
        embed.set_author(name="Error: No warning channel found!\nSet it with >wchannel [channel]!", icon_url=xmark)
        await ctx.send(embed=embed)
        return
    v1="\u200b"
    userid = str(user.id)
    if userid not in config[server]:
        config[server][userid] = dict()
        config[server][userid]["warnings"] = 0
        config[server][userid]["name"] = dict()
        config[server][userid]["name"] = str(user)
    config[server][userid]["name"] = str(user)
    num = config[server][userid]["warnings"]
    config[server][userid]["warnings"] = int(num) + 1
    num2 = config[server][userid]["warnings"]  # New number
    channelID = config[server]["channel"]
    channel = bot.get_channel(int(channelID.replace("<", "").replace(">", "").replace("#", "")))
    if "[here]" in reason:
        channel = ctx.channel
        reason = reason.replace("[here]", "")
    embed = discord.Embed(colour=embedcolour)
    embed.set_thumbnail(url=user.avatar_url)
    embed.set_author(name=f"Warning #{num2}", icon_url=exclamation)
    embed.add_field(name="User:", value=f"<@{userid}>", inline=True)
    embed.add_field(name="Warned by:", value=f"<@!{ctx.author.id}>", inline=True)
    embed.add_field(name="Channel:", value=f"<#{ctx.channel.id}>", inline=True)
    embed.add_field(name="Reason:", value=reason, inline=True)
    try:
        await channel.send(embed=embed)
    except:
        await senderror(ctx, "Error: The bot cannot send messages in the selected warning channel!\nChange it with `>warnc [channel]` or give the bot permissions!")
        return
    embed = discord.Embed(colour=embedcolour)
    embed.set_author(name="User has been warned.", icon_url=checkmark)
    embed.set_footer(text=f"{user} now has {int(num)+1} warnings.", icon_url=user.avatar_url)
    await ctx.send(embed=embed)
    write_file(config, "warnconfig.txt")

@warn.error
async def warn_error(ctx, error):
    if isinstance(error, CheckFailure):
        await senderror(ctx, "You are missing the Manage Messages permission!")

#@bot.command(name="warns")
async def warns(ctx, user:discord.Member):
    config = read_file("warnconfig.txt")
    server = str(ctx.guild.id)
    num = config[server][str(user.id)]["warnings"]
    embed = discord.Embed(colour=embedcolour)
    embed.set_author(name="", icon_url=bsquare)
    await ctx.send(embed=embed)

@has_permissions(administrator=True)
@bot.command(aliases=["uwarn"])
async def unwarn(ctx, id):
    #print("ki")
    config = read_file("warnconfig.txt")
    server = str(ctx.guild.id)
    warnchannel = config[server]["channel"]
    warnchannel = warnchannel.replace("<", "").replace(">", "").replace("#", "") # Turns channel from <#12345> to 12345
    warnchannelget = await bot.fetch_channel(int(warnchannel))
    try:
        msg = await warnchannelget.fetch_message(id)
    except:
        chanList = ctx.guild.channels
        for channel in chanList:
            try:
                msg = await channel.fetch_message(id)
                break
            except:
                continue
    id = msg
    embeds = id.embeds
    user = embeds[0].fields[0].value
    userid = str(user).replace("<", "").replace("@", "").replace(">", "")
    config = read_file("warnconfig.txt")
    num = config[server][userid]["warnings"]
    config[server][userid]["warnings"] = int(num) - 1
    num2 = config[server][userid]["warnings"]  # New number
    await id.delete()
    write_file(config, "warnconfig.txt")
    embed = discord.Embed(colour=embedcolour)
    embed.set_author(name="Successfully removed warning.", icon_url=checkmark)
    embed.set_footer(text=f"{user} now has {num2} warnings.")
    await ctx.send(embed=embed)

@unwarn.error
async def unwarn_error(ctx, error):
    if isinstance(error, CheckFailure):
        await senderror(ctx, "You are missing the Administrator permission!")

#@bot.event  # Nicholas
async def on_message_edit(before, after):
    if before.content == '':
        return
    embed = discord.Embed(colour=embedcolour)
    embed.set_author(name=f'Message Edited by {before.author.name}', icon_url=bsquare)
    embed.add_field(name='Before', value=before.content, inline=False)
    embed.add_field(name='After', value=after.content, inline=False)

    temp_channel = before.channel

    await temp_channel.send(embed=embed)

#@bot.event
async def on_message_delete(message):
    embed = discord.Embed(colour=embedcolour)
    embed.set_author(name=f'Message Deleted by {message.author.name} in {message.channel.name}', icon_url=bsquare)
    embed.add_field(name='Message', value=message.content)
    await message.channel.send(embed=embed)


# Discord
@bot.command(name="getmoji")
async def getmoji(ctx, emoji: discord.Emoji):
    embed = discord.Embed(colour=embedcolour)
    embed.set_image(url=emoji.url)
    await ctx.send(embed=embed)

@getmoji.error
async def getmoji_error(ctx, error):
    await senderror(ctx, "Error: Emoji not found!\nThis currently only works with server custom emojis!")

@has_permissions(manage_nicknames=True)
@bot.command(name="nick")
async def nick(ctx, user: discord.Member="None", *, newnick="None"):
    if user == "None":
        await senderror(ctx, "Please input the 'user' paramater!")
        return
    if newnick == "None":
        await senderror(ctx, "Please input the 'newnick' paramater!")
        return
    try:
        await user.edit(nick=newnick)
    except:
        await senderror(ctx, "You are not allowed to change this user's nickname!")
        return
    await sendcheck(ctx, f"Successfully changed nickname for {user}.")

@nick.error
async def nick_error(ctx, error):
    if isinstance(error, CheckFailure):
        await senderror(ctx, "You are missing the Manage Nicknames permission!")

@bot.command(name="avatar")  # Gets the user avatar of mentioned user
async def avatar(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author
    img = user.avatar_url
    embed = discord.Embed(colour=embedcolour, title="User Avatar for {}:".format(user), url="{}".format(img))
    embed.set_image(url=img)
    await ctx.send(embed=embed)

@bot.command(aliases=["davatar"])  # Gets the default user avatar of mentioned user
async def defavatar(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author
    img = user.default_avatar_url
    embed = discord.Embed(colour=embedcolour, title="Default Avatar for {}:".format(user), url="{}".format(img))
    embed.set_image(url=img)
    await ctx.send(embed=embed)

@avatar.error
async def avatar_error(ctx, error):
    await senderror(ctx, "Error: User not found!")

@bot.command(aliases=["user"])  # User information command.
async def userinfo(ctx, *, user: discord.Member):
    if user is None:
        user = ctx.author
    img = user.avatar_url
    userid = user.id
    serverjoindate = user.joined_at.strftime('%c ')
    toprole = user.top_role.id
    rolecolour = user.top_role.color
    numroles = len(user.roles)  # actually 1 less than this number.
    joindate = user.created_at.strftime('%c ')
    statusmsg = user.activity

    if user.bot:
        usertype = "Bot"
    else:
        usertype = "Human"

    status = user.status
    #print(status)
    if status == discord.Status.online:
        print("online")
    status = str(status).capitalize()

    online = bot.get_emoji(721873982927929384)
    idle = bot.get_emoji(721873982613225472)
    dnd = bot.get_emoji(721873982772740148)
    offline = bot.get_emoji(721873982894243921)
    streaming = bot.get_emoji(721873982801969162)

    if status == "Online":
        status = "{} ".format(online) + status
    elif status == "Idle":
        status = "{} ".format(idle) + status
    elif status == "Dnd":
        status = "Do Not Disturb"
        status = "{} ".format(dnd) + status
    elif status == "Streaming":
        status = "{} ".format(streaming) + status
    elif status == "Offline":
        status = "{} ".format(offline) + status

    config = read_file("warnconfig.txt")
    server = str(ctx.guild.id)
    if not str(user.id) in config[server]:
        num = "0"
    else:
        num = config[server][str(user.id)]["warnings"]

    v1 = "\u200b"
    embed = discord.Embed(color=rolecolour, description="**Information for <@{}>**".format(userid))
    embed.set_thumbnail(url=user.avatar_url)

    embed.add_field(name="Basic Information", value="Global Username:\nStatus:\nID:\nUser type:\nIcon URL:\nDiscord Join Date")
    embed.add_field(name=v1, value=v1, inline=True)
    embed.add_field(name=v1, value='{}\n{}\n{}\n{}\n>avatar\n{}'.format(user, status, userid, usertype, joindate))

    embed.add_field(name="Server-specific Information", value="Server Join Date:\n Top Role:\nNumber of roles:\nNumber of warns:")
    embed.add_field(name=v1, value=v1, inline=True)
    embed.add_field(name=v1, value='{}\n<@&{}>\n{}\n{}'.format(serverjoindate, toprole, numroles-1, num))

    await ctx.send(embed=embed)

@userinfo.error
async def userinfo_error(ctx, error):
    await senderror(ctx, "Error: User not found!")

@has_permissions(create_instant_invite=True)
@bot.command(name="invite")  # Generates a never-expiring invite link.
async def invite(ctx, channel:discord.TextChannel="None"):
    if channel == "None":
        await senderror(ctx, "Please input the 'channel' argument!")
        return
    url = await channel.create_invite(max_age=0)
    await ctx.send(url)

@invite.error
async def invite_error(ctx, error):
    if isinstance(error, CheckFailure):
        await senderror(ctx, "You are missing the Create Instant Invite permission!")
    else:
        await senderror(ctx, "Error: Channel not found!")


@bot.command(name='serveravatar')  # Gets the avatar of the server.
async def serveravatar(ctx):
    name = ctx.guild.name
    link = ctx.guild.icon_url
    embed = discord.Embed(color=embedcolour, title="Server Avatar for {}:".format(name), url=str(link))
    #embed.set_author(name='Server Avatar for {}'.format(name), icon_url="bot_icon")
    embed.set_image(url=ctx.guild.icon_url)
    await ctx.send(embed=embed)

@bot.command(aliases=["server"])  # Server info command.
async def serverinfo(ctx):
    name = ctx.guild.name
    link = ctx.guild.icon_url
    members = ctx.guild.member_count
    owner = ctx.guild.owner_id
    emojis = ctx.guild.emojis
    roles = ctx.guild.roles
    rolecount = len(roles)
    emojicount = len(emojis)
    date = ctx.guild.created_at.strftime('%c ')
    channels = len(ctx.guild.text_channels) + len(ctx.guild.voice_channels)
    textchannels = len(ctx.guild.text_channels)
    voicechannels = len(ctx.guild.voice_channels)
    id = ctx.guild.id

    users = 0
    bots = 0
    for i in ctx.guild.members: # Gets number of users and bots.
        if i.bot:
            bots = bots+1
        else:
            users = users+1

    a1 = 0
    count = 1
    for i in ctx.guild.members: # Gets names of administrators.
        if i.permissions_in(ctx.channel).administrator:
            if not i.bot:
                if not i.id == owner:
                    a1 = str(a1) + ", " + str(i.id)
        count = count + 1
        if count > int(members):
            break
    if not isinstance(a1, int):
        admins = a1.split(", ")
        admincounter = 1
        list = " "
        while admincounter < len(admins):
            list = list + "<@" + admins[admincounter] + ">" + "\n"
            admincounter = admincounter + 1
    else:
        list = "None"

    v1 = '\u200b'
    v2 = '\u200b'
    v3 = '\u200b'
    embed = discord.Embed(color=embedcolour, title="Server Information for\n*{}*".format(name))
    embed.set_thumbnail(url=link)

    embed.add_field(name="Leadership:", value="Owner:\nAdministrators:", inline=True)
    embed.add_field(name=v2, value=v3, inline=True)
    embed.add_field(name=v1, value="<@{}>\n{}".format(owner, list))

    embed.add_field(name="Statistics:", value="Total Members:\nUsers:\nBots:\nRoles:\nEmojis:\nTotal Channels:\nText Channels:\nVoice Channels:", inline=True)
    embed.add_field(name=v2, value=v3, inline=True)
    embed.add_field(name=v1, value="{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(members,users,bots,rolecount,emojicount,channels,textchannels,voicechannels), inline=True)

    embed.add_field(name="Other:", value="ID:\nCreated on:\nAvatar URL:", inline=True)
    embed.add_field(name=v2, value=v3, inline=True)
    embed.add_field(name=v1, value="{}\n{}\n>serveravatar".format(id, date), inline=True)

    await ctx.send(embed=embed)

@bot.command(aliases=["channel"])
async def channelinfo(ctx, chan:discord.TextChannel="None"):
    if chan == "None":
        chan = ctx.channel
    id = chan.id
    catid = chan.category_id
    created = chan.created_at.strftime('%c ')
    category = chan.category
    nsfw = chan.is_nsfw()
    position = str(int(chan.position) + 1)
    desc = chan.topic
    if category == "None":
        category = "N/A"
    if catid == "None":
        catid = "N/A"
    if desc == "":
        desc = "N/A"
    slow = chan.slowmode_delay
    if int(slow) > 3599:
        slow = str(math.trunc(int(slow)/60/60)) + "h"
    elif int(slow) > 59:
        slow = str(math.trunc(int(slow)/60)) + "m"
    elif int(slow) < 1:
        slow = "None"
    else:
        slow = str(slow) + "s"
    v1="\u200b"
    embed = discord.Embed(color=embedcolour, description=f"Information for <#{id}>")
    embed.add_field(name="Basic Information:", value="ID:\nCategory:\nCategory ID:\nCreated on:\nNSFW?\nPosition:\nSlowmode:", inline=True)
    embed.add_field(name=v1, value=v1, inline=True)
    embed.add_field(name=v1, value=f"{id}\n{category}\n{catid}\n{created}\n{nsfw}\n{position}\n{slow}", inline=True)
    embed.add_field(name="Description:", value=desc, inline=True)
    await ctx.send(embed=embed)

@bot.command(aliases=["roles", "rolelist"])  # Server role list
async def serverroles(ctx):
    roles = ctx.guild.roles
    name = ctx.guild.name
    admin = " "
    admin2 = " "
    f1 = " " # Formatted ID of role
    f2 = " " # Formatted ID of managed role
    assignments = " "
    assignments2 = " "
    count = 1
    for i in roles:
        if i.permissions.administrator:
            if i.managed:
                admin2 = "Yes" + "\n" + admin2
            else:
                admin = "Yes" + "\n" + admin
        else:
            if i.managed:
                admin2 = "No" + "\n" + admin2
            else:
                admin = "No" + "\n" + admin
        if i.name == "@everyone":
            f1 = "@everyone" + "" \
                               "\n" + f1
        else:
            if i.managed:
                f2 = "<@&" + str(i.id) + ">\n" + f2
            else:
                f1 = "<@&" + str(i.id) + ">\n" + f1
        if i.managed:
            assignments2 = assignments2 + "\n" + assignments2
        else:
            assignments = str(len(i.members)) + "\n" + assignments
        count = count + 1
        if count > len(roles):
            break

        # Splitting the fields into 3
    f1 = f1.split("\n")
    admin = admin.split("\n")
    assignments = assignments.split("\n")
    f1_1 = ""
    f1_2 = ""
    admin_1 = ""
    admin_2 = ""
    assignments_1 = ""
    assignments_2 = ""
    i = 0
    while i < len(f1):
        if i < 35:
            f1_1 = f1_1 + f1[i] + "\n"
            admin_1 = admin_1 + admin[i] + "\n"
            assignments_1 = assignments_1 + assignments[i] + "\n"
        else:
            f1_2 = f1_2 + f1[i] + "\n"
            admin_2 = admin_2 + admin[i] + "\n"
            assignments_2 = assignments_2 + assignments[i] + "\n"
        i += 1


        
    v1 = "\u200b"
    embed = discord.Embed(color=embedcolour, title="List of roles for *{}*".format(name))

    embed.add_field(name="Normal Roles:", value=f1_1)
    embed.add_field(name=v1, value=v1)
    embed.add_field(name="Admin?", value=admin_1)

    embed.add_field(name=v1, value=f1_2)
    embed.add_field(name=v1, value=v1)
    embed.add_field(name=v1, value=admin_2)

    embed2 = discord.Embed(color=embedcolour, title="List of roles for *{}*".format(name))
    embed2.add_field(name="Managed Roles:", value=f2)
    embed2.add_field(name=v1, value=v1)
    embed2.add_field(name="Admin?", value=admin2)
    await ctx.send(embed=embed)
    await ctx.send(embed=embed2)

@bot.command(aliases=["role"])
async def roleinfo(ctx, role: discord.Role):
    members = role.members
    positioninv = role.position
    colour = role.colour
    roleid = role.id
    permissions = role._permissions
    permissions = discord.Permissions(permissions=permissions)
    #print(members)

    i = iter(permissions)
    res = "None"
    res2 = "\u200b"
    c = 0
    test = 1
    while test == 1:
        #print(a[0])
        a = next(i, None)
        a = str(a)
        a = a.replace("(", "")
        a = a.replace(")", "")
        a = a.replace("'", "")
        a = a.split(", ")
        res1 = str(a[0])
        res1 = res1.replace("_", " ")
        res1 = res1.title()
        res1 = res1.replace("Tts", "TTS")
        res1 = res1.replace("External Emojis", "Use External Emojis")
        try:
            if str(a[1]) == "True":
                c = c+1
                f = (len(res.split("\n")))
                if not (c % 2) == 0:
                    if res == "None":
                        res = ""
                    res = res1 + "\n" + str(res)
                else:
                    res2 = res1 + "\n" + str(res2)
        except IndexError:
            break

    position = len(ctx.guild.roles) - positioninv

    v1 = "\u200b"
    embed = discord.Embed(color=colour, description=" **Information for** <@&{}>".format(roleid))

    embed.add_field(name="Statistics", value="Position:\nColour (Hexadecimal):\nID:", inline=True)
    embed.add_field(name=v1, value=v1, inline=True)
    embed.add_field(name=v1, value="{}\n{}\n{}".format(position, colour, roleid), inline=True)

    embed.add_field(name="Permissions", value="{}".format(res), inline=True)
    embed.add_field(name=v1, value=v1, inline=True)
    embed.add_field(name=v1, value="{}".format(res2), inline=True)

    await ctx.send(embed=embed)

# String
@bot.command(name='reverse')  # Inverts the input.
async def reverse(ctx, *arg):
    if not arg:
        await missingargs(ctx)
        return
    if ' '.join(arg) == '<:st:701862311610024248>':
        arg = '<:st_inverted:701861523735183500>'
    elif ' '.join(arg) == '<:st_inverted:701861523735183500>':
        arg = '<:st:701862311610024248>'
    else:
        arg = (' '.join(arg)[::-1])
    await ctx.send(arg)

@bot.command(name='repeat')
async def rp(ctx, *, arg):
    #await ctx.message.delete()
    await ctx.send(arg)

@bot.command(name='delay')
async def delay(ctx, time, *arg):
    msg=(" ".join(arg))
    now = datetime.datetime.now()
    print("> DELAY: {} || Message '{}' sent by {} in channel '{}' with a delay of {} seconds in '{}'".format(now, msg, ctx.message.author, ctx.channel, time, ctx.guild.name))
    print("> DELAY: {} || Message '{}' sent by {} in channel '{}' with a delay of {} seconds in '{}'".format(now, msg, ctx.message.author, ctx.channel, time, ctx.guild.name),file=open('log.txt', 'a'))
    await asyncio.sleep(int(time))
    await ctx.send(" ".join(arg))

@bot.command(name='ptc')  # Prints input without formatting.
async def ptc(ctx, *string):
    print(' '.join(string))
    await ctx.send("```{}```".format(' '.join(string)))

@bot.command(name='len')  # Finds the length of input..
async def length(ctx, *str):
    str = ' '.join(str)
    await ctx.send(len(str))

@bot.command(name='binary')  # Converts input to binary
async def binary(ctx, *num):
    num = ' '.join(num)
    try: #integer to binary
        int(num)
        if int(num) < 0:
            await ctx.send("Number must be greater than -1!")
            return
        temp = num
        res = ' '
        while int(temp) > 0:
            res = str(int(temp) % 2) + res
            temp = str(int(temp) // 2)
        await ctx.send("`{}` converted to binary is:\n```{}```".format(num, res))
    except ValueError: #text to binary
        res = [format(ord(i), 'b') for i in num]
        nres = ''
        for i in res:
            while len(i) < 7:
             i = '0' + i
            nres += i
        # print the nres
        await ctx.send("`{}` converted to binary is:\n```{}```".format(num, nres))

@bot.command(name='ascii')  # Converts input to ASCII
async def ascii(ctx, *str):
    str = ' '.join(str)
    res = ' '.join(format(ord(i)) for i in str)
    await ctx.send("`{}` converted to ASCII is:\n```{}```".format(str, res))

def b10helper(s):
    num = 0
    for c in s:
        num = num << 1 | int(c)
    return chr(num)

@bot.command(name='b10')  # Converts binary to ASCII
async def b10(ctx, s):
    res = ''
    for i in range(0, len(s), 7):
        res += b10helper(s[i:i+7])

    await ctx.send(''.join(res))

@bot.command(name="estring")
async def estring(ctx, type, *, arg = "no"):
    if arg == "no":
        await senderror(ctx, "You are missing the 'arg' parameter!")
        return
    res = ""
    for i in arg:
        if re.search(r"[A-Za-z]", i):
            res += f":regional_indicator_{i.lower()}: "
        elif re.search(r"[0-9]", i):
            res += f":{num2words(int(i))}:"
        elif i == " ":
            res += " "
        else:
            res += i
    if str(type) == "s":
        await ctx.send("\u200b" + res)
    elif str(type) == "p":
        embed = discord.Embed(colour=embedcolour, description=f"```{res}```")
        await ctx.send(embed=embed)
    else:
        await senderror(ctx, "Error: Invalid 'type' parameter!")
        return

@bot.command(name="morse")
async def morse(ctx, arg, *, input):
    input = input.upper()
    if not arg:
        await senderror(ctx, "Error: Please specify 'encode' or 'decode'!")
        return

    morse = read_file("morse.json")
    morse_decrypt = {v: k for k, v in morse["encrypt"].items()}

    result = ""

    if arg == "encode":
        for i in input.split(" "):  # For each word
            for j in i:  # For each letter in word
                if j == "\n":
                    result += "\n"
                else:
                    result += morse["encrypt"][j] + " "
            result += "/ "
        result += "end"
        result = result.replace(" / end","")
    elif arg == "decode":
        for i in input.split(" / "):  # For each word
            print(i)
            for j in i.split(" "):  # For each letter in word
                print(j)
                if j == "\n":
                    result += "\n"
                else:
                    result += morse_decrypt[j]
            result += " "
        result += "end"
        result = result.replace(" end", "")
    embed = discord.Embed(colour=embedcolour)
    embed.add_field(name="Original:", value=f"```{input.lower()}```", inline=False)
    embed.add_field(name="Converted:", value=f"```{result}```", inline=False)
    await ctx.send(embed=embed)

@morse.error
async def morse_error(ctx,error):
    if isinstance(error, ValueError):
        await senderror(ctx, "Error: Invalid input!")

# Math
@bot.command(name='roll')  # Returns random number in range
async def roll(ctx, s, e):  # S = start, E = end
    if float(s) == 0:
        await ctx.send("Number cannot be 0!")
        return
    if float(e) == 0:
        await ctx.send("Number cannot be 0!")
        return
    res = random.randrange(float(s), float(e), 1)
    await ctx.send(res)

@bot.command(name='flip')  # Flips a coin.
async def flip(ctx):
    possibilities = ["The coin never landed.", "You somehow flipped it too hard and now its in orbit.", "Congratulations! You flipped heads!", "You flipped heads. That sucks.", "Landed on heads.", "Heads up.", "It is heads.", "The coin landed on heads!", "Heads!", "Heads it is!", "It landed with tails facing down.", "You flipped heads.", "Congratulations! You flipped tails!", "You flipped tails. That sucks.", "Landed on tails.", "Tails up.", "It is tails.", "The coin landed on tails!", "Tails!", "Tails it is!", "It landed with heads facing down.", "You flipped tails.", "Somehow, it landed on the edge!"]
    await ctx.send(random.choice(possibilities ))

# Web
@bot.command(name='google')  # Searches Google for things.
async def google(ctx, *args):
    args = '+'.join(args)
    await ctx.send("https://www.google.com/search?q={}".format(args))

@bot.command(name='yt')  # Searches YouTube for things.
async def yt(ctx, *args):
    args = '+'.join(args)
    await ctx.send("https://www.youtube.com/results?search_query={}".format(args))

@bot.command(name='define')  # Searches Dictionary.com for things.
async def define(ctx, *args):
    args = '-'.join(args)
    await ctx.send("https://www.dictionary.com/browse/{}".format(args))

@bot.command(name='overflow')  # Searches Stack Overflow for things.
async def overflow(ctx, *args):
    args = '+'.join(args)
    await ctx.send("https://stackoverflow.com/search?q={}".format(args))

# Science
@bot.command(name="element")
async def element(ctx, arg):
    try:
        int(arg)
        r = requests.get(url="https://neelpatel05.pythonanywhere.com/element/atomicnumber",params={"atomicnumber":arg}) # Atomic number
    except ValueError:
        if len(arg) < 4:
            r = requests.get(url="https://neelpatel05.pythonanywhere.com/element/symbol", params={"symbol":arg}) # Symbol
        else:
            r = requests.get(url="https://neelpatel05.pythonanywhere.com/element/atomicname", params = {"atomicname":arg}) # Name
    data = r.json()

    try:
        ename = data['name']
    except KeyError:
        await ctx.send("NoSuchElementException")
        return

    symbol = data['symbol']
    number = data['atomicNumber']
    mass1 = data['atomicMass']
    mass = mass1[0:5]
    boil = data['boilingPoint']
    melt = data['meltingPoint']
    ion = data['oxidationStates']
    state1 = data['standardState']
    state = state1.capitalize()
    density = data['density']
    discovered = data['yearDiscovered']
    unknown = False
    try:
        neutrons = round(float(mass) - float(number))
        meltc = round(melt-273.15, 2)
        boilc = round(boil-273.15, 2)
    except TypeError:
        neutrons = "Unknown"
        meltc = "Unknown"
        boilc = "Unknown"
        unknown = True

    for i in data.keys():
        if not data[i]:
            data[i] = "Unknown"

    v1 = "\u200b"
    embed = discord.Embed(color=embedcolour, title=ename, url="https://en.wikipedia.org/wiki/{}".format(ename))

    embed.add_field(name="Symbol", value=symbol, inline=True)
    embed.add_field(name="Number:", value=number, inline=True)
    embed.add_field(name="Mass:", value=mass, inline=True)

    embed.add_field(name="Basic Information", value="Protons:\nElectrons:\nNeutrons:\nIon Charges:", inline=True)
    embed.add_field(name=v1, value="{}\n{}\n{}\n{}".format(number, number, neutrons, ion), inline=True)
    embed.add_field(name=v1, value=v1, inline=True)

    embed.add_field(name="Temperature Information", value="Melting Point:\nBoiling Point\nStandard State:", inline=True)
    if unknown == False:
        embed.add_field(name=v1, value="{}°C\n{}°C\n{}\n".format(meltc, boilc, state), inline=True)
    else:
        embed.add_field(name=v1, value="{}\n{}\n{}\n".format(meltc, boilc, state), inline=True)
    embed.add_field(name=v1, value=v1, inline=True)

    embed.add_field(name="Other Information", value="Year Discovered:\nDensity:", inline=True)
    embed.add_field(name=v1, value="{}\n{} g/cm3".format(discovered, density), inline=True)
    embed.add_field(name=v1, value=v1, inline=True)

    await ctx.send(embed=embed)

@bot.command(name="apod")  # NASA Atronomy Picture of the Day
async def apod(ctx):
    key = "5qYeNbxprCSgNDe05owe1vBo2SlrjSo1jLvDzbOf"
    r = requests.get(url="https://api.nasa.gov/planetary/apod?api_key={}".format(key))
    data = r.json()
    title = data['title']
    img = data['hdurl']
    desc = data['explanation']
    v1 = "\u200b\u200b\u200b\u200b\u200b\u200b\u200b\u200b\u200b\u200b\u200b\u200b\u200b\u200b"
    embed = discord.Embed(colour=embedcolour, title=title, url="https://apod.nasa.gov/apod/astropix.html", description=desc)
    embed.set_image(url=img)
    embed.add_field(name=v1, value=v1, inline=True)
    embed.add_field(name=v1, value=v1, inline=True)
    embed.add_field(name=v1, value=v1, inline=True)
    await ctx.send(embed=embed)

@bot.command(name="ap")  # NASA Astronomy Picture
async def rapod(ctx):
    key = "5qYeNbxprCSgNDe05owe1vBo2SlrjSo1jLvDzbOf"
    r = requests.get(url="https://api.nasa.gov/planetary/apod?api_key={}".format(key))
    data = r.json()
    title = data['title']
    img = data['hdurl']
    desc = data['explanation']
    date = data['date']
    embed = discord.Embed(colour=embedcolour, title=title, url="https://apod.nasa.gov/apod/astropix.html")
    embed.set_image(url=img)
    embed.add_field(name="Description:", value=desc)
    await ctx.send(embed=embed)

@bot.command(name="cb")
async def cb(ctx, name):
    r = requests.get(url="https://api.le-systeme-solaire.net/rest/bodies/{}".format(name))
    try:
        data = r.json()
    except:
        await ctx.send("404: Celestial Body Not Found. (maybe check spelling?)")

    name = data['englishName']
    isPlanet = data['isPlanet']
    if isPlanet == True:
        type = "Planet"
    elif isPlanet == False:
        type = "Moon"
    else:
        type = "Error"
    moonlist = data['moons']
    try:
        moons = len(moonlist)
    except TypeError:
        moons = "0"
    escape = data['escape']  # m/s
    radius = data['meanRadius']
    escape = data['escape']
    vol = data['vol']
    vol = str(vol)
    vol = vol.replace("{", "")
    vol = vol.replace("}", "")
    vol = vol.replace("'volValue':", "")
    vol = vol.replace("'volExponent':", "")
    vol = vol.replace(" ", "")
    vol = vol.split(",")
    volValue = vol[0]
    volExp = vol[1]
    year = data['sideralOrbit']
    dayh = data['sideralRotation']  # hours
    day = round(dayh/24, 2)  # Earth days
    ecc = data['eccentricity']
    mass = data['mass']
    mass = str(mass)
    mass = mass.replace("{", "")
    mass = mass.replace("}", "")
    mass = mass.replace("'massValue':", "")
    mass = mass.replace("'massExponent':", "")
    mass = mass.replace(" ", "")
    mass = mass.split(",")
    massValue = mass[0]
    massExp = mass[1]
    orbiting1 = data['aroundPlanet']
    orbiting1 = str(orbiting1)
    orbiting1 = orbiting1.replace("{", "")
    orbiting1 = orbiting1.replace("}", "")
    orbiting1 = orbiting1.replace("'planet':", "")
    orbiting1 = orbiting1.replace("'rel':", "")
    orbiting1 = orbiting1.replace(" ", "")
    orbiting1 = orbiting1.split(",")
    orbiting = orbiting1[0]
    orbiting = orbiting.replace("'", "")
    orbiting = orbiting.capitalize()
    if orbiting == "None":
        orbiting = "The Sun"
    gravity = data['gravity']  # m/s2
    gs = round(gravity*0.10197, 2)  # G units
    escape = data['escape']  # m/s
    inc = data['inclination']
    ap = data['aphelion']
    pe = data['perihelion']

    v1 = "\u200b"
    link = "https://en.wikipedia.org/wiki/{}_(planet)".format(name)
    embed = discord.Embed(colour=embedcolour, title=name, url=link)

    embed.add_field(name="Designations", value="Type:\nOrbiting around:\nNumber of natural satellites:\nEccentricity:\nInclination:\nOrbital period:\nRotational period:\nEscape Velocity\nApoapsis:\nPeriapsis:", inline=True)
    embed.add_field(name=v1, value=v1, inline=True)
    embed.add_field(name=v1, value="{}\n{}\n{}\n{}\n{} deg\n{} days\n{} days\n{} m/s\n{} km\n{} km".format(type, orbiting, moons, ecc, inc, year, day, escape, ap, pe), inline=True)

    embed.add_field(name="Physical Characteristics", value="Average Diameter:\nVolume:\nMass:\nSurface Gravity:", inline=True)
    embed.add_field(name=v1, value=v1, inline=True)
    embed.add_field(name=v1, value="{} km\n{}x10^{} km3\n{}x10^{} kg\n{}g".format(radius*2, volValue, volExp, massValue, massExp, gs), inline=True)

    embed.set_footer(text="Days are in Earth days.")
    await ctx.send(embed=embed)

# Fun
@bot.command(name="cat")
async def cat(ctx, arg = "None"):
    if arg.capitalize() == "F":
        arg = "Fact"
    if arg == "None":
        r = requests.get("https://api.thecatapi.com/v1/images/search")
        data = r.json()
        link = data[0]['url']
        embed = discord.Embed(colour=embedcolour)
        embed.set_image(url=link)
        await ctx.send(embed=embed)
    elif arg.capitalize() == "Fact":
        r = requests.get("https://some-random-api.ml/facts/cat")
        data = r.json()
        text = data["fact"]
        embed = discord.Embed(colour=embedcolour, description=text)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(colour=embedcolour, description="**Invalid argument!**\n`[leave blank]` : Image\n`fact` : Fact")
        await ctx.send(embed=embed)

@bot.command(name="dog")
async def dog(ctx, arg = "None"):
    if arg.capitalize() == "F":
        arg = "Fact"
    if arg == "None":
        r = requests.get("https://api.thedogapi.com/v1/images/search")
        data = r.json()
        link = data[0]['url']
        embed = discord.Embed(colour=embedcolour)
        embed.set_image(url=link)
        await ctx.send(embed=embed)
    elif arg.capitalize() == "Fact":
        r = requests.get("https://some-random-api.ml/facts/dog")
        data = r.json()
        text = data["fact"]
        embed = discord.Embed(colour=embedcolour, description=text)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(colour=embedcolour, description="**Invalid argument!**\n`[leave blank]` : Image\n`fact` : Fact")
        await ctx.send(embed=embed)

@bot.command(name="bird")
async def bird(ctx, arg = "None"):
    if arg.capitalize() == "F":
        arg = "Fact"
    if arg == "None":
        r = requests.get("https://some-random-api.ml/img/birb")
        data = r.json()
        link = data['link']
        embed = discord.Embed(colour=embedcolour)
        embed.set_image(url=link)
        await ctx.send(embed=embed)
    elif arg.capitalize() == "Fact":
        r = requests.get("https://some-random-api.ml/facts/bird")
        data = r.json()
        text = data["fact"]
        embed = discord.Embed(colour=embedcolour, description=text)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(colour=embedcolour, description="**Invalid argument!**\n`[leave blank]` : Image\n`fact` : Fact")
        await ctx.send(embed=embed)
        
@bot.command(name="fox")
async def fox(ctx, arg = "None"):
    if arg.capitalize() == "F":
        arg = "Fact"
    if arg == "None":
        r = requests.get("https://some-random-api.ml/img/fox")
        data = r.json()
        link = data['link']
        embed = discord.Embed(colour=embedcolour)
        embed.set_image(url=link)
        await ctx.send(embed=embed)
    elif arg.capitalize() == "Fact":
        r = requests.get("https://some-random-api.ml/facts/fox")
        data = r.json()
        text = data["fact"]
        embed = discord.Embed(colour=embedcolour, description=text)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(colour=embedcolour, description="**Invalid argument!**\n`[leave blank]` : Image\n`fact` : Fact")
        await ctx.send(embed=embed)
        
@bot.command(name="panda")
async def panda(ctx, arg = "None"):
    if arg.capitalize() == "F":
        arg = "Fact"
    if arg == "None":
        r = requests.get("https://some-random-api.ml/img/panda")
        data = r.json()
        link = data['link']
        embed = discord.Embed(colour=embedcolour)
        embed.set_image(url=link)
        await ctx.send(embed=embed)
    elif arg.capitalize() == "Fact":
        r = requests.get("https://some-random-api.ml/facts/panda")
        data = r.json()
        text = data["fact"]
        embed = discord.Embed(colour=embedcolour, description=text)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(colour=embedcolour, description="**Invalid argument!**\n`[leave blank]` : Image\n`fact` : Fact")
        await ctx.send(embed=embed)

@bot.command(name="koala")
async def koala(ctx, arg = "None"):
    if arg.capitalize() == "F":
        arg = "Fact"
    if arg == "None":
        r = requests.get("https://some-random-api.ml/img/koala")
        data = r.json()
        link = data['link']
        embed = discord.Embed(colour=embedcolour)
        embed.set_image(url=link)
        await ctx.send(embed=embed)
    elif arg.capitalize() == "Fact":
        r = requests.get("https://some-random-api.ml/facts/koala")
        data = r.json()
        text = data["fact"]
        embed = discord.Embed(colour=embedcolour, description=text)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(colour=embedcolour, description="**Invalid argument!**\n`[leave blank]` : Image\n`fact` : Fact")
        await ctx.send(embed=embed)

@bot.command(name="kill")
async def kill(ctx, user, *killer):
    if not killer:
        r = open("kill.txt", "r")
    else:
        r = open("killbyuser.txt", "r")

    killer = " ".join(killer)

    r = r.read()
    f = r.split("\n")
    method = random.choice(f)
    method = method.replace("[user]", user)
    method = method.replace("[killer]", killer)

    if not '<@' in user:
        await ctx.send("Error 403: Forbidden: You cannot kill a non-user!")
        return
    else:
        if '<@!521086131132039169>' in user or "<@!327948165468782595>" in user or '<@521086131132039169>' in user or "<@327948165468782595>" in user:
            await ctx.send("Error 403 Forbidden: That user is blacklisted from death and therefore is immortal.")
        else:
            await ctx.send("{}.".format(method))

@bot.command(name="punch")
async def punch(ctx, user):
    if not '<@' in user:
        await ctx.send("Error 403: Forbidden: You cannot punch a non-user!")
        return
    else:
        if user == '<@!521086131132039169>':
            await ctx.send("Error 403: Forbidden: You cannot punch me!")
        else:
            await ctx.send('{} got punched by {}!'.format(user, ctx.message.author.mention))

@bot.command(name="8ball")
async def ball(ctx, arg):
    responses=["Most definitely.","Definitely not.","Think and try again.","Probably.","Probably not.","There is a chance.","There is no chance.","Error 404: Response Not Found.","You can count on it.","Don't count on it."]
    await ctx.send(random.choice(responses))

# Gaming
riotkey = "RGAPI-be4feda7-047c-45ca-89a0-4980665d1ff1"
region = "na1"

@bot.command(name="summoner")
async def summoner(ctx, name):
    await ctx.send("Gathering information, please wait...")
    watcher = LolWatcher(riotkey)
    try:
        data = watcher.summoner.by_name(region, name)
    except:
        await senderror(ctx, "User not found!")
    name = data["name"]
    userID = data["id"]
    accountID = data["accountId"]
    iconID = data["profileIconId"]
    iconLink = f"http://ddragon.leagueoflegends.com/cdn/10.18.1/img/profileicon/{iconID}.png"
    level = data["summonerLevel"]
    data2 = watcher.champion_mastery.by_summoner(region, userID)
    data2 = data2[0]
    champID = data2["championId"]
    champLevel = data2["championLevel"]
    champPoints = data2["championPoints"]  # Total number of champion points for this player and champion combination - they are used to determine championLevel.
    champCurrentPoints = data2["championPointsSinceLastLevel"]  # Current number of points in current level.
    champPointsUntil = data2["championPointsUntilNextLevel"]  # Number of points until next level.
    champTotalLevelPoints = champCurrentPoints + champPointsUntil  # Total number of points required to advance to next level
    progress = f"{champCurrentPoints} / {champTotalLevelPoints}"

    r = requests.get(url="http://ddragon.leagueoflegends.com/cdn/10.18.1/data/en_US/champion.json")
    data3 = r.json()
    for i in data3["data"]:
        champName = i
        currentID = data3["data"][i]["key"]
        if int(currentID) == int(champID):
            break

    try:
        data4 = watcher.match.matchlist_by_account(region, accountID)  # List of last 100 matches.
        matchData = "Yes"
    except:
        matchData = "Unavailable"
    kills = 0
    deaths = 0
    assists = 0
    matchcount = 0
    await ctx.send("test1")
    for match in reversed(data4["matches"]):  # Check each game/match
        gameID = match["gameId"]
        matchcount += 1
        #print(matchcount)
        #await ctx.send("ki1")
        data5 = watcher.match.by_id(region, gameID)  # Game Information
        #await ctx.send("ki2")
        for identity in data5["participantIdentities"]:  # For each identity...
            if identity["player"]["accountId"] == accountID:  # If the correct player is found...
                pID = identity["participantId"]  # Saves the Participant ID
                break

        for participant in data5["participants"]:  # For each participant...
            if participant["participantId"] == pID:  # If the participant's ID is correct...
                kills = kills + participant["stats"]["kills"]  # Adds kills
                deaths = deaths + participant["stats"]["deaths"]  # Adds deaths
                assists = assists + participant["stats"]["assists"]  # Adds assists
                break


    kdar = f"{round((kills+assists)/deaths, 3)}:1"

    v1="\u200b"
    embed = discord.Embed(colour=embedcolour, title=f"Summoner Stats for {name}")
    embed.set_thumbnail(url=iconLink)
    embed.add_field(name="Info", value="Level:")
    embed.add_field(name=v1, value=v1)
    embed.add_field(name=v1, value=level)
    embed.add_field(name="Stats (Last 100 games)", value="Kills:\nDeaths:\nAssists:\nKDA Ratio:")
    embed.add_field(name=v1, value=v1)
    embed.add_field(name=v1, value=f"{kills}\n{deaths}\n{assists}\n{kdar}")
    embed.add_field(name="Mastery", value="Highest Champion:\nChampion Level:\nLevel Progress:")
    embed.add_field(name=v1, value=v1)
    embed.add_field(name=v1, value=f"{champName}\n{champLevel}\n{progress}")
    await ctx.send(embed=embed)

# Other
@bot.command(name="time")  # Gets the time and date.
async def time(ctx):
    now = datetime.datetime.now().strftime('%c ')
    await ctx.send('The current date and time is: ```{}```'.format(now))

@bot.command(name="poll")
async def poll(ctx, *arg):
    await ctx.message.delete()
    author = ctx.author
    content = ctx.message.content
    await author.send(f"Here's your recent poll command, in case you want to copy and paste it again:\n{content}")
    list, text, desc, endson = " ".join(arg).split(",,")
    embed = discord.Embed(colour=embedcolour, description=text)
    pollcreator = ctx.message.author
    desc = desc.replace("\n", "\n")
    img = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(pollcreator)
    embed.set_footer(text="Poll created by {}".format(pollcreator), icon_url=img)
    embed.add_field(name="Description:", value=desc)
    if not endson.capitalize().strip() == "Never":
        embed.add_field(name="Ends on:", value=endson, inline=False)

    message = await ctx.send(embed=embed)
    msg_id = message.id
    msg = await ctx.channel.fetch_message(msg_id)
    list = list.replace(" ",", ")
    list = list.replace("️", "")
    counter = 0
    list = list.split(', ')
    while counter < len(list):
        await msg.add_reaction(list[counter])
        counter = counter + 1

@bot.command(aliases=["pollhelp"])
async def pollinfo(ctx):
    embed = discord.Embed(colour=embedcolour)
    embed.set_author(name="Poll Command Information")
    embed.add_field(name="Formatting and Syntax", value=">poll `reaction emojis` ,, `title text` ,, `description` ,, `end date`", inline=False)
    embed.add_field(name="Example:", value=f">poll {checkmarkmoji} {xmarkmoji} ,, Example: yes or no? ,, React with {checkmarkmoji} for yes, {xmarkmoji} for no. ,, 2222/13/33", inline=False)
    await ctx.send(embed=embed)
    # Poll example
    embed = discord.Embed(colour=embedcolour, description="Example: yes or no?")
    pollcreator = bot.user
    img = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(pollcreator)
    embed.set_footer(text="Poll created by {}".format(pollcreator), icon_url=img)
    embed.add_field(name="Description:", value=f"React with {checkmarkmoji} for yes, {xmarkmoji} for no.")
    embed.add_field(name="Ends on:", value="2222/13/33", inline=False)
    message = await ctx.send(embed=embed)
    msg_id = message.id
    msg = await ctx.channel.fetch_message(msg_id)
    await msg.add_reaction(checkmarkmoji)
    await msg.add_reaction(xmarkmoji)

@bot.command(name="makepoll")
async def makepoll(ctx, id):
    msg = await ctx.channel.fetch_message(id)
    await ctx.message.delete()
    await msg.add_reaction(checkmarkmoji)
    await msg.add_reaction(xmarkmoji)

@bot.command(name="makevotes")
async def makevotes(ctx, id):
    msg = await ctx.channel.fetch_message(id)
    await ctx.message.delete()
    await msg.add_reaction(upvotemoji)
    await msg.add_reaction(downvotemoji)

# Unlisted
@bot.command(name="react")
async def react(ctx, switch, id, emoji):
    msg = await ctx.channel.fetch_message(id)
    if switch == "add" or switch == "a":
        await ctx.message.delete()
        await msg.add_reaction(emoji)
        return
    elif switch == "remove" or switch == "r":
        await ctx.message.delete()
        await msg.remove_reaction(emoji, bot.user)
    else:
        await ctx.send("Invalid input!")

@bot.command()  # makes bot send custom animated emoji (lyndon)
async def amoji(ctx, ID):
    await ctx.send(f"{bot.get_emoji(int(ID))}")
    # await ctx.message.delete()

@bot.command(name='command')
async def command(ctx):
    embed=discord.Embed(colour=embedcolour)
    embed.add_field(name="Embed name now white!", value="Easier to read than the previous grey!")
    await ctx.send(embed=embed)

@bot.command(name='error')
async def error(ctx):
    await ctx.send("error")

@bot.command(name='rp')
async def rp(ctx, *, arg):
    await ctx.send('$'+arg)

@bot.command(name='hax')  # hacks Bill's bot [FIXED]
async def hax(ctx, member, amount):
    await ctx.send("$capture <@519326187491950593>")
    await ctx.send("$daily")
    await ctx.send("$weekly")
    await asyncio.sleep(0.5)
    await ctx.send("$give {} {}".format(member, amount))
    await ctx.send('$work')
    await ctx.send("$capture <@519326187491950593>")

@bot.command(name="rst")
async def rst(ctx):
    f = open("squaretwitters.txt", "r")
    f = f.read()
    f = f.split("\n")
    res = str(random.choice(f))

    embed = discord.Embed(colour=embedcolour)
    embed.set_image(url=res)
    await ctx.send(embed=embed)

data = read_file("config.json")
token = data["testtoken"]
bot.run(token)