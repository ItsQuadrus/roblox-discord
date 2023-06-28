import logging
import json
import requests
import time


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
