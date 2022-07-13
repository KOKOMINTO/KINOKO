import discord
from discord.ext import slash
from discord.ext import tasks
from datetime import datetime
import os
import dotenv
import sqlite3

dotenv.load_dotenv()
TOKEN = os.environ['TOKEN']
con = sqlite3.connect('Kinoko.db')
cur = con.cursor()
bot = slash.SlashBot(command_prefix="!",intents=discord.Intents().all())

reactionroleOpt = []
reminderOpt = []

reactionroleOpt.append(slash.Option(description='Type the ID of the message you wish to use',type=3,required=True))
reactionroleOpt.append(slash.Option(description='Channel where the message is located',type=7,required=True))
reactionroleOpt.append(slash.Option(description='Type the emoji you wish to use (can use default and custom ones)',type=3,required=True))
reactionroleOpt.append(slash.Option(description='Ping the role you wish to use',type=8,required=True))

reminderOpt.append(slash.Option(description='Channel where the reminder will be sent',type=7,required=True))
reminderOpt.append(slash.Option(description='Message you wish to send as a reminder',type=3,required=True))
reminderOpt.append(slash.Option(description='Time and date to set for the reminder (YYYY-MM-DD HH:MM)',type=3,required=True))
reminderOpt.append(slash.Option(description='How often the reminder will be repeated, in hours (optional)',type=4,required=False))

@bot.slash_cmd()
async def reactionroleset(ctx: slash.Context, message: reactionroleOpt[0], channel: reactionroleOpt[1], reaction: reactionroleOpt[2], role: reactionroleOpt[3]):
    """Create a new reaction role"""
    cur.execute("INSERT INTO ReactionRole VALUES (?, ?, ?, ?);", (channel.id, message, reaction, role.id))
    con.commit()
    full_message = await channel.fetch_message(int(message))
    await ctx.respond("Reaction role added!")
    await full_message.add_reaction(reaction)

@bot.slash_cmd()
async def reminderset(ctx: slash.Context, channel: reminderOpt[0], message: reminderOpt[1], time: reminderOpt[2], delay: reminderOpt[3]):
    """Create a new reminder"""
    cur.execute("INSERT INTO Reminder VALUES (?,?,?,?);",(channel.id, message, time, delay))
    con.commit()
    await ctx.respond("Reminder added!")

@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    message = str(payload.message_id)
    if member is not bot.user:
        cur.execute("SELECT emoji, role FROM ReactionRole WHERE message = ?;",[message])
        rows = cur.fetchall()
        for row in rows:
            if str(payload.emoji) == str(row[0]):
                role = guild.get_role(int(row[1]))
                await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    message = str(payload.message_id)
    if member is not bot.user:
        cur.execute("SELECT emoji, role FROM ReactionRole WHERE message = ?;",[message])
        rows = cur.fetchall()
        for row in rows:
            if str(payload.emoji) == str(row[0]):
                role = guild.get_role(int(row[1]))
                await member.remove_roles(role)

@tasks.loop(minutes=1.0)
async def check_reminder():
    timestamp = datetime.now()
    timestamp = timestamp.strftime(r"%Y-%m-%d %H:%M")
    cur.execute("SELECT message,channel FROM Reminder WHERE strftime('%Y-%m-%d %H:%M',time) = ?;",[timestamp])
    rows = cur.fetchall()
    for row in rows:
        channel = bot.get_channel(int(row[1]))
        await channel.send(str(row[0]))

check_reminder.start()
bot.run(TOKEN)
con.close()

