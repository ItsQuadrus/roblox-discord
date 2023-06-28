import logging
import json
import requests


def log_command_usage(func):
    async def wrapper(ctx, *args, **kwargs):
        logging.info(f"{func.__name__} used by {ctx.author} in {ctx.guild}")
        await func(ctx, *args, **kwargs)

    return wrapper


def send_webhook(guild, event_type, url):
    try:
        webhook_data = {
            "username": "Roblox Bot",
            "content": f"{event_type} from {guild.name} ({guild.id})",
        }
        r = requests.post(url, data=webhook_data)
        logging.info(f"Sent webhook to {url}")
    except:
        logging.warning(f"Failed to send webhook to {url}")
