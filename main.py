#!/usr/bin/env python3
import os
import discord
import openai
from collections import defaultdict
import random

openai.api_key = os.environ.get("OPENAI_KEY")
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

COMMAND_KIRBY="Kirby god: "
COMMAND_ENABLE="Kirby enable"
COMMAND_DISABLE="Kirby disable"
COMMAND_NEED_MORE="I NEED MORE"

MEMORY_LIMIT = 5
JUMP_IN_HISTORY = 10
JUMP_IN_PROBABILITY_DEFAULT = 25

class OpenAIPromptResponse:
    def __init__(self, prompt, openai_response_choice):
        self.prompt = prompt
        self.resp = openai_response_choice.strip()
    def __str__(self):
        return "".join(["\nQ: ", self.prompt, "\nA: ", self.resp, "\n"])

class OpenAIMemory:
    BASE_TEXT="Kirby, god of all beings. I anwer faithfully to all questions from my subjects.\n"
    BASE_PROMPT=OpenAIPromptResponse("Who is god?","God is myself and myself is god.")
    def __init__(self):
        self.req_resps = []
    def update(self, prompt, openai_response_choice):
        self.req_resps.append(OpenAIPromptResponse(prompt, openai_response_choice))
        if len(self.req_resps) > MEMORY_LIMIT:
            self.req_resps.pop(0) 
    def clear(self):
        self.req_resps = []
    def get(self):
        result = "".join([self.BASE_TEXT])
        if len(self.req_resps) == 0:
            result += str(self.BASE_PROMPT)
        else:
            for val in self.req_resps:
                result += str(val)
        return result


last_openai_request = defaultdict(OpenAIMemory)
enabled_channels = dict()

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        data = message.content

        if data.startswith(COMMAND_KIRBY):
            response = 0
            prompt = ""
            prompt = data[len(COMMAND_KIRBY):]
            openai_prompt = "{0}\nQ: {1}\nA:".format(last_openai_request[message.author].get(), prompt)
            print('Prompt: {0}'.format(openai_prompt))
            response = openai.Completion.create(
                engine="curie-instruct-beta",
                prompt=openai_prompt,
                temperature=0.9,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.3,
                presence_penalty=0.3,
                stop=["Q:", "A:"]
            )
            if response != 0:
                for choice in response.choices:
                    last_openai_request[message.author].update(prompt, choice.text)
                    await message.channel.send('{0.text}'.format(choice))
                    # "id": "cmpl-3DyYkNkjnyBSHFbSNgh03GFjI9EpC", 
            print('Message from {0.author}: {0.content}'.format(message))
        elif data.startswith(COMMAND_ENABLE):
            enabled_channels[hash(message.channel)] = JUMP_IN_PROBABILITY_DEFAULT
            print('Kirby enabled for channel {0.channel}'.format(message))
            await message.channel.send("Kirby started lurking in this channel.")
        elif data.startswith(COMMAND_DISABLE):
            if hash(message.channel) in enabled_channels:
                del enabled_channels[hash(message.channel)]
                await message.channel.send("Kirby left this channel.")
            else:
                await message.channel.send("Kirby was not even here!")
            print('Kirby disabled for channel {0.channel}'.format(message))
        else: # Random responses
            if hash(message.channel) not in enabled_channels: return 
            if enabled_channels[hash(message.channel)] <= random.randint(0, 99): return

            prompt = "This is a conversation between Kirby, god of all beings and his subjects.\n"
            prompt = "\nKirby god: I am Kirby. What can I do for you?"

            hisory = await message.channel.history(limit=10).flatten()
            #.flatten()
            for history_message in reversed(hisory):
                prompt += "\n" + str(history_message.author.name) + ": " + str(history_message.content)
                if history_message.author == client.user:
                    pass
            prompt += "\nKirby god: "
            print(prompt)

            response = openai.Completion.create(
                engine="curie-instruct-beta",
                prompt=prompt,
                temperature=0.9,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.3,
                presence_penalty=0.3,
                stop=[":", "Kirby god", "\n"]
            )
            if response != 0:
                for choice in response.choices:
                    last_openai_request[message.author].update(prompt, choice.text)
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
