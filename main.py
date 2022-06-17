import discord
from discord.ext import slash
import os
import dotenv
import json
#import sqlite3

dotenv.load_dotenv()
TOKEN = os.environ['TOKEN']
f = open("save.json","r+")
allReactionRole = json.load(f)
#con = sqlite3.connect('save.db')
bot = slash.SlashBot(command_prefix="!",intents=discord.Intents().all())

messageOpt = slash.Option(description='Type the ID of the message you wish to use',type=3,required=True)
channelOpt = slash.Option(description='Channel where the message is located',type=7,required=True)
reactionOpt = slash.Option(description='Type the emoji you wish to use',type=3,required=True)
roleOpt = slash.Option(description='Ping the role you wish to use',type=8,required=True)

@bot.slash_cmd()
async def reactionroleset(ctx: slash.Context, message: messageOpt, channel: channelOpt, reaction: reactionOpt, role: roleOpt):
    """Create a new reaction role"""
    emoji=bot.get_emoji(reaction)
    reactionrole = {"message":message,"channel":channel.id,"reaction":reaction,"role":role.id}
    allReactionRole["reactionrole"].append(reactionrole)
    f.seek(0, 0)
    json.dump(allReactionRole,f)
    f.truncate()
    full_message = await channel.fetch_message(int(message))
    await ctx.respond("Reaction role added!")
    await full_message.add_reaction(reaction)

@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if member != bot.user:
        for x in range(len(allReactionRole['reactionrole'])):
            if str(payload.emoji) == str(allReactionRole['reactionrole'][x]['reaction']) and str(payload.message_id) == str(allReactionRole['reactionrole'][x]['message']):
                role = guild.get_role(int(allReactionRole['reactionrole'][x]['role']))
                await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if member is not bot.user:
        for x in range(len(allReactionRole['reactionrole'])):
            if str(payload.emoji) == str(allReactionRole['reactionrole'][x]['reaction']) and str(payload.message_id) == str(allReactionRole['reactionrole'][x]['message']):
                role = guild.get_role(int(allReactionRole['reactionrole'][x]['role']))
                await member.remove_roles(role)

bot.run(TOKEN)
f.close()
