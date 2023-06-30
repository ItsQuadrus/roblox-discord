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
from functions import send_webhook
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


# Roblox
COOKIE = os.environ["COOKIE"]
ROBLOX_USER_ID = int(os.environ["ROBLOX_USER_ID"])

# Misc
utc_now = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S UTC")

# Discord user ID
DISCORD_USER_ID = int(os.environ["DISCORD_USER_ID"])

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


@bot.command()
async def friends(ctx):  # friends command
    logging.info("Friends command called...")
    headers = {
        "Cookie": COOKIE,  # Raw cookie from roblox.com, contains .ROBLOSECURITY but is not limited to it.
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate, br",  # Accept-Encoding header
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",  # User-Agent header
    }
    r = requests.get(  # GET request to friends API, in order to get friends online, and to get their PlaceID and FriendID
        f"https://friends.roblox.com/v1/users/{ROBLOX_USER_ID}/friends/online",
        headers=headers,
    )

    if r.status_code == 200:  # if HTTP 200 OK
        data = r.json()  # extract JSON data from response
        if len(data["data"]) == 0:  # if no friends are online
            await ctx.send("No friends online.")  # send message
        else:
            embed = discord.Embed(  # create embed
                title="Friends online",
                description=f"Friends online for this [roblox user](https://www.roblox.com/users/{ROBLOX_USER_ID}/profile)",
                color=0x00FF00,  # green color means online
            )
            for friend in data["data"]:  # for each friend online
                PlaceID = friend["userPresence"]["placeId"]  # PlaceID
                FriendID = friend["id"]  # FriendID

                friend_ids = [
                    friend["id"] for friend in data["data"]
                ]  # list of friend IDs, this will help us to get presence

                if (  # if friend is on the website, don't show the game URL as they are not in a game
                    friend["userPresence"]["lastLocation"] == "Website"
                ):
                    value = f"{friend['userPresence']['lastLocation']}"
                else:
                    presence_url = "https://presence.roblox.com/v1/presence/users"
                    request_data = json.dumps(
                        {"userIds": friend_ids}
                    )  # convert to JSON
                    logging.info(
                        "JSON data for request to presence.roblox.com: " + request_data
                    )
                    request_presence = requests.post(
                        url=presence_url, headers=headers, data=request_data
                    )  # POST request to presence API, in order to get UniverseID
                    presenceData = (
                        request_presence.json()
                    )  # extract JSON data from response
                    logging.info("Presence data: " + str(presenceData))
                    if request_presence.status_code == 200:
                        rootPlaceId = presenceData["userPresences"][0][
                            "rootPlaceId"
                        ]  # extract rootPlaceId from response
                        GameURL = f"{discord.utils.escape_markdown(f'https://www.roblox.com/games/start?placeId={PlaceID}&launchData=%7B%22roomId%22%3A%20{rootPlaceId}%7D')}"  # create game URL using PlaceID and UniverseID
                        value = f"{friend['userPresence']['lastLocation']} - Join them [here]({GameURL})"  # value of embed, with GameURL
                    else:
                        value = f"{friend['userPresence']['lastLocation']} - ||Couldn't get UniverseID: {request_presence.status_code}||"
                        logging.warning(
                            "Couldn't get UniverseID: "
                            + str(request_presence.status_code)
                        )

                embed.add_field(  # a field per friend
                    name=friend["displayName"],
                    value=value,
                    inline=False,
                )
            await ctx.send(embed=embed)  # send embed
            logging.info("Friends command completed. Sent embed.")
    else:
        if r.status_code == 401:
            await ctx.send(
                f"Error 401: Unauthorized. Make sure your cookie is still valid. <@{DISCORD_USER_ID}>"
            )
            logging.warning(
                "Error 401: Unauthorized. Make sure your cookie is still valid."
            )
        elif r.status_code == 429:
            await ctx.send("Error 429: Rate limited. Please wait!")
            logging.warning("Error 429: Rate limited. Please wait!")
        else:
            await ctx.send(f"Error {r.status_code}")
            logging.warning(f"Error {r.status_code}: {r.text}")


@bot.command()
async def status(ctx):
    logging.info("Status command called...")
    headers = {
        "Cookie": COOKIE,  # Raw cookie from roblox.com, contains .ROBLOSECURITY but is not limited to it.
        "Content-Type": "application/json",
    }
    url = "http://hostedstatus.com/1.0/status/59db90dbcdeb2f04dadcf16d"
    r = requests.get(url)
    if r.status_code == 200:
        parsed_data = json.loads(r.text)
        overall_status = parsed_data["result"]["status_overall"]["status"]

        embed = discord.Embed(title="Roblox Status", description=f"As of {utc_now}", color=0x00ff00)
        embed.add_field(name="Overall Status", value=overall_status, inline=True)
        for status in r.json()["result"]["status"]:
            for container in status["containers"]:
                embed.add_field(name=container["name"], value=container["status"], inline=True)
        await ctx.send(embed=embed)
    else:
        logging.warning(f"API Error, error code {r.status_code}")
        await ctx.send(f"API Error, error code {r.status_code}")
    
        
    
    
    


bot.run(os.environ["DISCORD_TOKEN"], log_handler=log_file_handler)
