#!/usr/bin/env python3
import os
import discord
import openai
from collections import defaultdict

openai.api_key = os.environ.get("OPENAI_KEY")
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

COMMAND_KIRBY="Kirby god: "
COMMAND_CURIE="Curie: "
COMMAND_BABBAGE="Babbage: "
COMMAND_ADA="Ada: "
COMMAND_NEED_MORE="I NEED MORE"

MEMORY_LIMIT = 5

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

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        data = message.content
        response = 0
        prompt = ""
        
        if data.startswith(COMMAND_KIRBY):
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
                
        if data.startswith(COMMAND_CURIE):
            prompt = data[len(COMMAND_CURIE):]
            response = openai.Completion.create(
                engine="curie",
                prompt="{0}\n".format(prompt),
                temperature=0.9,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.3,
                presence_penalty=0.3,
                stop=["\n\n"]
            )
                
        if data.startswith(COMMAND_ADA):
            prompt = data[len(COMMAND_ADA):]
            response = openai.Completion.create(
                engine="babbage",
                prompt="{0}\n".format(prompt),
                temperature=0.9,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.3,
                presence_penalty=0.3,
                stop=["\n\n"]
            )

        if data.startswith(COMMAND_BABBAGE):
            prompt = data[len(COMMAND_BABBAGE):]
            response = openai.Completion.create(
                engine="ada",
                prompt="{0}\n".format(prompt),
                temperature=0.9,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.3,
                presence_penalty=0.3,
                stop=["\n\n"]
            )

        if response != 0:
            for choice in response.choices:
                last_openai_request[message.author].update(prompt, choice.text)
                await message.channel.send('{0.text}'.format(choice))
                # "id": "cmpl-3DyYkNkjnyBSHFbSNgh03GFjI9EpC", 
        print('Message from {0.author}: {0.content}'.format(message))

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.guilds = True
intents.reactions = True
client = MyClient(intents=intents)
client.run(DISCORD_BOT_TOKEN)
