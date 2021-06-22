OpenAI Discord bot
==================

This is an OpenAI discord bot.

Environment keys:
- OPENAI_KEY
- DISCORD_BOT_TOKEN

Usage
=============

There are currently 4 commands:
- "Kirby god: " => Answers as a Kirby god. 
- "Curie: "
- "Babbage: "
- "Ada: "

Installation
==========

```bash
git clone https://github.com/AlexisTM/gpt3-discord-bot

cd gpt3-discord-bot

export DISCORD_BOTOKEN="sometoken" 
export OPENAI_KEY="someothertoken"

python3 main.py
```

Create a bot application: https://discordpy.readthedocs.io/en/stable/discord.html

Configure intents for your bot: https://discordpy.readthedocs.io/en/stable/intents.html

In the oauth section of discord dev portal, make a link to allow your bot to join your server such as:

https://discord.com/api/oauth2/authorize?client_id=APPID&permissions=2215115840&scope=bot

In this case, we only need the bot scope and READ/WRITE messages permissions/
