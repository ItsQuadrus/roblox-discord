# Roblox Discord

This discord bot looks up your friends on Roblox and tells you who is online. It also has a cool feature that allows you to see what games they are playing.

## Commands

- `.rd help` - Shows a list of commands
- `.rd online` or `.rd playing` - Shows a list of your friends that are online or playing a game (outputs the same thing)

### Example

`.rd online`

```
Online Friends (2):
- @builderman - 156
- @Roblox - 1

Playing Friends (1):
- @bobby - 238929308021 - Playing: Arsenal

```

## Setup

1. `git clone https://github.com/ItsQuadrus/roblox-discord.git`
2. `python3 -m venv venv`
3. `source venv/bin/activate` or `venv\Scripts\activate.bat`
4. `pip install -r requirements.txt`
5. `cp .env.example .env` or `copy .env.example .env`
6. Fill in the `.env` file with your credentials.
7. `python3 bot.py`
8. Invite the bot to your server and run the commands
9. Enjoy!

## Special thanks

This project wouldn't be possible without this [list of API endpoints](https://roblox.fandom.com/wiki/List_of_web_APIs). Thanks to the people who made it!

## License

This project is licensed under the [Creative Commons Attribution 3.0 Unported License](https://creativecommons.org/licenses/by/3.0/).

You are free to use this code for any purpose, commercial or non-commercial. **Attribution is required: you must give credit to the original author.**

You also need to **indicate if changes were made.** e.g. "Translation of BonkBot by ItsQuadrus"
