#!/usr/bin/env python3
import os
import discord
import openai

openai.api_key = os.environ.get("OPENAI_KEY")
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

COMMAND_KIRBY="Kirby god: "
COMMAND_CURIE="Curie: "
COMMAND_BABBAGE="Babbage: "
COMMAND_ADA="Ada: "

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        data = message.content
        if data.startswith(COMMAND_KIRBY):
            data = data[len(COMMAND_KIRBY):]
            response = openai.Completion.create(
                engine="curie-instruct-beta",
                prompt="I am Kirby god and will anwer faithfully to questions. My subject is asking me the following:\n{0}\n".format(data),
                temperature=0.9,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.3,
                presence_penalty=0.3,
                stop=["\n"]
            )
            print(response)
            for choice in response.choices:
                await message.channel.send('{0.text}'.format(choice))
                
        if data.startswith(COMMAND_CURIE):
            data = data[len(COMMAND_CURIE):]
            response = openai.Completion.create(
                engine="curie",
                prompt="{0}\n".format(data),
                temperature=0.9,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.3,
                presence_penalty=0.3,
                stop=["\n"]
            )
            print(response)
            for choice in response.choices:
                await message.channel.send('{0.text}'.format(choice))
                
        if data.startswith(COMMAND_ADA):
            data = data[len(COMMAND_ADA):]
            response = openai.Completion.create(
                engine="babbage",
                prompt="{0}\n".format(data),
                temperature=0.9,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.3,
                presence_penalty=0.3,
                stop=["\n"]
            )
            print(response)
            for choice in response.choices:
                await message.channel.send('{0.text}'.format(choice))

        if data.startswith(COMMAND_BABBAGE):
            data = data[len(COMMAND_BABBAGE):]
            response = openai.Completion.create(
                engine="ada",
                prompt="{0}\n".format(data),
                temperature=0.9,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.3,
                presence_penalty=0.3,
                stop=["\n"]
            )
            print(response)
            for choice in response.choices:
                await message.channel.send('{0.text}'.format(choice))
        print('Message from {0.author}: {0.content}'.format(message))

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.guilds = True
intents.reactions = True
client = MyClient(intents=intents)
client.run(DISCORD_BOT_TOKEN)