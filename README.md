OpenAI Discord bot
==================

This is an OpenAI discord bot replying as Kirby.

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
python3 -m pip install -r requirements.txt --user

export DISCORD_BOTOKEN="sometoken" 
export OPENAI_KEY="someothertoken"

python3 main.py
```

NOTES
==========

- If your Kirby is replying the same thing over and over, `Kirby clean` it.
- If it continues, you can fix it by enforcing default prompts. I wanted to keep only the "personal" history thus remove the base prompt once one custom prompt exists. If you are giving two prompts asking for similar responses, you risk falling in a loop.
   - Fix 1: Keep the default prompts for until you can fill it with personal prompts
   - Fix 2: Always keep default prompts   
- This is very light, I run this on a PiZero and it replies almost instantly (but it is only on 10 or so servers).

Technical help on how to make a Discord bot:
==================

Create a bot application: https://discordpy.readthedocs.io/en/stable/discord.html

Configure intents for your bot: https://discordpy.readthedocs.io/en/stable/intents.html

In the oauth section of discord dev portal, make a link to allow your bot to join your server such as:

https://discord.com/api/oauth2/authorize?client_id=APPID&permissions=2215115840&scope=bot

In this case, we only need the bot scope and READ/WRITE messages permissions/
