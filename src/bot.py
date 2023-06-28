# Roblox-Discord Bot by ItsQuadrus
# Licensed under Attribution 3.0 Unported (CC BY 3.0) license. Availaible at https://creativecommons.org/licenses/by/3.0/legalcode
# This bot is not affiliated with Discord or Roblox in any way.

# User ID of bot: 1123612094227550310
# Bot invite link: https://discord.com/api/oauth2/authorize?client_id=1123612094227550310&permissions=0&scope=bot
# API Used: https://friends.roblox.com/docs/

import discord
from discord.ext import commands
import logging
import datetime
from dotenv import load_dotenv
import os
from functions import log_command_usage, send_webhook
import sys
import json
import requests

# Load environment variables
load_dotenv()

try:
    webhook_url = os.environ[
        "WEBHOOK_LOG"
    ]  # What's this? This is a webhook URL for logging. This is optional, but recommended to know what's going on with your bot.
except KeyError:
    logging.warn("No webhook URL provided. Continuing without webhook.")

ROBLOX_USER_ID = os.environ["ROBLOX_USER_ID"]
# Discord bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".rd ", intents=intents)
bot.remove_command("help")

# Logging
log_folder = "logs"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)
log_file_name = (
    f"{log_folder}/bot_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log_file_handler = logging.FileHandler(log_file_name, encoding="utf-8", mode="w")

"""
EVENTS
"""


# Bot is online
@bot.event
async def on_ready():
    logging.info("Bot is online.")
    await bot.change_presence(activity=discord.Game("Roblox"))


# PREFIX MANAGEMENT (prefix.json)
@bot.event
async def on_guild_join(guild):  # when bot is added to a guild
    logging.info(f"Bot joined a guild: {guild.name} ({guild.id})")
    send_webhook(guild=guild, event_type="ADDED_TO_GUILD", url=webhook_url)


@bot.event
async def on_guild_remove(guild):  # when bot is removed from a guild
    logging.info(f'Bot left a guild: "{guild.name}" ({guild.id})')
    send_webhook(guild=guild, event_type="REMOVED_FROM_GUILD", url=webhook_url)


"""
COMMANDS
"""


# Ping command
@bot.command()
async def ping(ctx):
    logging.info(f"ping used by {ctx.author} in {ctx.guild}")
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")


"""
    Example response:
    {
  "data": [
    {
      "userPresence": {
        "UserPresenceType": "Online",
        "UserLocationType": "Page",
        "lastLocation": "Website",
        "placeId": null,
        "rootPlaceId": null,
        "gameInstanceId": null,
        "universeId": null,
        "lastOnline": "2023-06-28Tx:x:x.x"
      },
      "id": x,
      "name": "abc",
      "displayName": "abcdefg"
    }
  ]
}

or

{"data":[{"userPresence":{"UserPresenceType":"InGame","UserLocationType":"Game","lastLocation":"Arsenal","placeId":286090429,"rootPlaceId":286090429,"gameInstanceId":"xxxxxx","universeId":xxxxx,"lastOnline":"2023-06-28Tx:x:x.xX"},"id":x,"name":"abc","displayName":"abcdefg"}]}
"""


@bot.command()
async def friends(ctx):
    headers = {"Cookie": os.environ["ROBLOX_TOKEN"]}
    r = requests.get(
        f"https://friends.roblox.com/v1/users/{ROBLOX_USER_ID}/friends/online",
        headers=headers,
    )
    if r.status_code == 200:
        data = r.json()
        if len(data["data"]) == 0:
            await ctx.send("No friends online.")
        else:
            embed = discord.Embed(
                title="Friends online",
                description=f"Friends online for this [roblox user](https://www.roblox.com/users/{ROBLOX_USER_ID}/profile)",
                color=0x00FF00,
            )
            for friend in data["data"]:
                embed.add_field(
                    name=friend["displayName"],
                    value=friend["userPresence"]["lastLocation"],
                    inline=False,
                )
            await ctx.send(embed=embed)
    else:
        await ctx.send(f"Error {r.status_code}")
        logging.warning(f"Error {r.status_code}")


bot.run(os.environ["DISCORD_TOKEN"], log_handler=log_file_handler)
