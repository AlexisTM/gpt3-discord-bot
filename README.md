OpenAI Discord bot
==================

NOTE: More features are available in the Rust version: https://github.com/AlexisTM/discord-god-rust

This is an OpenAI discord bot replying as Kirby.

Environment keys:
- OPENAI_KEY
- AI21_API_KEY
- DISCORD_BOT_TOKEN

Come and test on Discord!: https://discord.gg/Y8XPcj2Q

Commands
=============

- `Kirby are you there?`: Replies yes if the server runs
- `Kirby enable`: Allow Kirby god to randomly jump into conversations (15% chance of reply)
    - `Kirby disable`: Disable the Kirby mode of the channel 
- `Kirby god: `: Answers as a Kirby god. 
    - Remembers the 5 last prompts & answers
    - Clean the memory with `Kirby clean`
- `Marv: ` => Answers as a chatbot that reluctantly answers questions. Not maintained ;)

Installation
==========

```bash
git clone https://github.com/AlexisTM/gpt3-discord-bot

cd gpt3-discord-bot
python3 -m pip install -r requirements.txt --user

export DISCORD_BOTOKEN="sometoken" 
export OPENAI_KEY="someothertoken"
export AI21_API_KEY="yetanothertoken"

python3 main.py
```

Notes: 
- You can directly speak to the bot for a direct chat to Kirby
- The 5 message memory is over the same channel. I will eventually add the user name in the memory for more coherence.
- AI21 is free with enough fun for a day, but is much less smart than OpenAI's version in my biased opinion.


![Wow, Kirby is so funny](doc/kirby.png)


Technical help on how to make a Discord bot:
==================

Create a bot application: https://discordpy.readthedocs.io/en/stable/discord.html

Configure intents for your bot: https://discordpy.readthedocs.io/en/stable/intents.html

In the oauth section of discord dev portal, make a link to allow your bot to join your server such as:

https://discord.com/api/oauth2/authorize?client_id=APPID&permissions=2215115840&scope=bot

In this case, we only need the bot scope and READ/WRITE messages permissions/
