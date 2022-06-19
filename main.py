import discord
from discord.ext import slash
import os
import dotenv
import sqlite3

dotenv.load_dotenv()
TOKEN = os.environ['TOKEN']
con = sqlite3.connect('save.db')
cur = con.cursor()
bot = slash.SlashBot(command_prefix="!",intents=discord.Intents().all())

messageOpt = slash.Option(description='Type the ID of the message you wish to use',type=3,required=True)
channelOpt = slash.Option(description='Channel where the message is located',type=7,required=True)
reactionOpt = slash.Option(description='Type the emoji you wish to use (can use default and custom ones)',type=3,required=True)
roleOpt = slash.Option(description='Ping the role you wish to use',type=8,required=True)

@bot.slash_cmd()
async def reactionroleset(ctx: slash.Context, message: messageOpt, channel: channelOpt, reaction: reactionOpt, role: roleOpt):
    """Create a new reaction role"""
    cur.execute("INSERT INTO ReactionRole VALUES (?, ?, ?, ?)", (channel.id, message, reaction, role.id))
    con.commit()
    full_message = await channel.fetch_message(int(message))
    await ctx.respond("Reaction role added!")
    await full_message.add_reaction(reaction)

@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    message = str(payload.message_id)
    if member is not bot.user:
        cur.execute("SELECT emoji, role FROM ReactionRole WHERE message = ?",[message])
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
        cur.execute("SELECT emoji, role FROM ReactionRole WHERE message = ?",[message])
        rows = cur.fetchall()
        for row in rows:
            if str(payload.emoji) == str(row[0]):
                role = guild.get_role(int(row[1]))
                await member.remove_roles(role)

bot.run(TOKEN)
con.close()

