import discord
import discord_slash
from discord_slash.utils.manage_commands import create_option
import os
import dotenv
import json
dotenv.load_dotenv()

TOKEN = os.environ['TOKEN']
f = open("save.json","r+")
allReactionRole = json.load(f)
bot = discord.Client(intents=discord.Intents().all())
command = discord_slash.SlashCommand(bot, sync_commands=True)

@command.slash(name = "reactionroleset", description = "Set reaction roles for a specific message",options = [
        create_option(
            name = "message",
            description = "Type the ID of the message you wish to use",
            option_type = 3,
            required = True
        ),
        create_option(
            name = "channel",
            description = "Channel where the message is located",
            option_type = 7,
            required = True
        ),
        create_option(
                    name="reaction",
                    description = "Type the emoji you wish to use",
                    required = True,
                    option_type = 3
        ),
        create_option(
                    name = "role",
                    description = "Ping the role you wish to use",
                    required = True,
                    option_type = 8
        )
    ]
)

async def reactionroleset(ctx, message, channel, reaction, role):
    emoji=bot.get_emoji(reaction)
    reactionrole = {"message":message,"channel":channel.id,"reaction":reaction,"role":role.id}
    allReactionRole["reactionrole"].append(reactionrole)
    f.seek(0, 0)
    json.dump(allReactionRole,f)
    f.truncate()
    full_message = await channel.fetch_message(int(message))
    await ctx.send(content="Reaction role added!")
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
