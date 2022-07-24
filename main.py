import discord
from discord.ext import slash, tasks
from datetime import datetime, timedelta
import os
import dotenv
import sqlite3

dotenv.load_dotenv()
TOKEN = os.environ['TOKEN']
con = sqlite3.connect('Kinoko.db')
cur = con.cursor()
bot = slash.SlashBot(command_prefix="!",intents=discord.Intents().all())

ReminderOpt = []
ReactionRoleOpt = []
WelcomeOpt = []
GoodbyeOpt = []

ReactionRoleOpt.append(slash.Option(description='ID of the message used',type=3,required=True))
ReactionRoleOpt.append(slash.Option(description='Channel of the message',type=7,required=True))
ReactionRoleOpt.append(slash.Option(description='Emoji used (default and custom compatible)',type=3,required=True))
ReactionRoleOpt.append(slash.Option(description='Ping role to give',type=8,required=True))

ReminderOpt.append(slash.Option(description='Channel of the reminder',type=7,required=True))
ReminderOpt.append(slash.Option(description='Content of the reminder',type=3,required=True))
ReminderOpt.append(slash.Option(description='Time and date (YYYYMMDDHHMM format)',type=4,required=True))
ReminderOpt.append(slash.Option(description='How often the reminder will be repeated (WDH format)',type=4,required=False))

WelcomeOpt.append(slash.Option(description='Welcoming channel',type=7,required=True))
WelcomeOpt.append(slash.Option(description='Joining message',required=True))

GoodbyeOpt.append(slash.Option(description='Leaving channel',type=7,required=True))
GoodbyeOpt.append(slash.Option(description='Goodbye message',type=3,required=True))

@bot.slash_cmd()
async def ping(ctx: slash.Context):
    """pong""" 
    await ctx.respond("pong")
    
@bot.slash_cmd()
async def welcomeset(ctx: slash.Context, channel: WelcomeOpt[0], message: WelcomeOpt[1]):
    """Set a welcoming message for new members"""
    cur.execute("INSERT OR REPLACE INTO Welcome VALUES (?,?,?);",(ctx.guild.id, channel.id, message))
    await ctx.respond("Welcome message added!")

@bot.slash_cmd()
async def goodbyeset(ctx: slash.Context, channel: GoodbyeOpt[0], message: GoodbyeOpt[1]):
    """Set a goodbye  message for leaving members"""
    cur.execute("INSERT OR REPLACE INTO Goodbye VALUES (?,?,?);",(ctx.guild.id, channel.id, message))
    await ctx.respond("Goodbye message added!")

@bot.slash_cmd()
async def reactionroleset(ctx: slash.Context, message: ReactionRoleOpt[0], channel: ReactionRoleOpt[1], reaction: ReactionRoleOpt[2], role: ReactionRoleOpt[3]):
    """Create a new reaction role"""
    cur.execute("INSERT INTO ReactionRole VALUES (?, ?, ?, ?);", (channel.id, message, reaction, role.id))
    con.commit()
    full_message = await channel.fetch_message(int(message))
    await ctx.respond("Reaction role added!")
    await full_message.add_reaction(reaction)

@bot.slash_cmd()
async def reminderset(ctx: slash.Context, channel: ReminderOpt[0], text: ReminderOpt[1], time: ReminderOpt[2], repeat: ReminderOpt[3]):
    """Create a new reminder"""
    cur.execute("INSERT INTO Reminder VALUES (?,?,?,?);",(channel.id, text, time, repeat))
    con.commit()
    await ctx.respond("Reminder added!")

@bot.slash_cmd()
async def goodbyeunset(ctx: slash.Context):
    """Disable goodbye message"""
    cur.execute("DELETE FROM Goodbye WHERE guild = ?;",[ctx.guild.id])
    await ctx.respond("Goodbye message disabled!")

@bot.slash_cmd()
async def welcomeunset(ctx: slash.Context):
    """Disable goodbye message"""
    cur.execute("DELETE FROM Welcome WHERE guild = ?;",[ctx.guild.id])
    await ctx.respond("Goodbye message disabled!")

@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if member is not bot.user:
        cur.execute("SELECT emoji, role FROM ReactionRole WHERE message = ?;",[str(payload.message_id)])
        rows = cur.fetchall()
        for row in rows:
            if str(payload.emoji) == str(row[0]):
                role = guild.get_role(int(row[1]))
                await member.add_roles(role)
@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if member is not bot.user:
        cur.execute("SELECT emoji, role FROM ReactionRole WHERE message = ?;",[str(payload.message_id)])
        rows = cur.fetchall()
        for row in rows:
            if str(payload.emoji) == str(row[0]):
                role = guild.get_role(int(row[1]))
                await member.remove_roles(role)

@bot.event
async def on_member_join(member):
    cur.execute("SELECT message, channel FROM Welcome WHERE guild = ?;",[str(member.guild.id)])
    rows = cur.fetchall()
    for row in rows:
        channel = bot.get_channel(int(row[1]))
        await channel.send(row[0])

@bot.event
async def on_member_remove(member):
    cur.execute("SELECT message, channel FROM Goodbye WHERE guild = ?;",[str(member.guild.id)])
    rows = cur.fetchall()
    for row in rows:
        channel = bot.get_channel(int(row[1]))
        await channel.send(row[0])

@tasks.loop(seconds=10.0)
async def check_reminder():
    timestamp = datetime.now()
    timestamp = int(timestamp.strftime(r"%Y%m%d%H%M"))
    cur.execute("SELECT ROWID,message,channel FROM Reminder WHERE time <= ?;",[timestamp])
    rows = cur.fetchall()
    for row in rows:
        channel = bot.get_channel(int(row[2]))
        cur.execute("UPDATE Reminder SET time = time + repeat  WHERE ROWID = ?;",[row[0]])
        await channel.send(str(row[1]))

check_reminder.start()
bot.run(TOKEN)
con.commit()
con.close()

