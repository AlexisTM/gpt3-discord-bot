OpenAI Discord bot
==================

This is an OpenAI discord bot.

Environment keys:
- OPENAI_KEY
- DISCORD_BOT_TOKEN

Commands
=============

- `Kirby are you there?`: Replies yes if the server runs
- `Kirby enable`: Allow Kirby god to randomly jump into conversations (15% chance of reply)
    - `Kirby disable`: Disable the Kirby mode of the channel 
- `Kirby god: `: Answers as a Kirby god. 
    - Remembers the 5 last prompts & answers
    - Clean the memory with `Kirby clean`
- `Marv: ` => Answers as a chatbot that reluctantly answers questions.


Installation
==========

```bash
git clone https://github.com/AlexisTM/gpt3-discord-bot

cd gpt3-discord-bot

export DISCORD_BOTOKEN="sometoken" 
export OPENAI_KEY="someothertoken"

python3 main.py
```

Technical help on how to make a Discord bot:
==================

Create a bot application: https://discordpy.readthedocs.io/en/stable/discord.html

Configure intents for your bot: https://discordpy.readthedocs.io/en/stable/intents.html

In the oauth section of discord dev portal, make a link to allow your bot to join your server such as:

https://discord.com/api/oauth2/authorize?client_id=APPID&permissions=2215115840&scope=bot

In this case, we only need the bot scope and READ/WRITE messages permissions/
