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
COMMAND_CLEAN="Kirby clean"
COMMAND_PRESENCE="Kirby are you there?"

MEMORY_LIMIT = 5
JUMP_IN_HISTORY = 10
JUMP_IN_PROBABILITY_DEFAULT = 15

COMMAND_SHAKESPEARE="Shakespeare: "

COMMAND_MARV="Marv: "
MARV_PROMPT = """Marv is a chatbot that reluctantly answers questions.
You: How many pounds are in a kilogram?
Marv: This again? There are 2.2 pounds in a kilogram. Please make a note of this.
You: What does HTML stand for?
Marv: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.
You: When did the first airplane fly?
Marv: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.
You: What is the meaning of life?
Marv: I’m not sure. I’ll ask my friend Google. Not to Bing, it would just say to buy Microsofts products.
You: {0}
Marv:"""


class OpenAIPromptResponse:
    def __init__(self, prompt, openai_response_choice):
        self.prompt = prompt
        self.resp = openai_response_choice.strip()
    def __str__(self):
        return "".join(["\nYou: ", self.prompt, "\nKirby: ", self.resp, "\n"])

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
            openai_prompt = "{0}\nYou: {1}\nKirby:".format(last_openai_request[message.author].get(), prompt)
            print('Prompt: {0}'.format(openai_prompt))
            response = openai.Completion.create(
                engine="curie-instruct-beta",
                prompt=openai_prompt,
                temperature=0.9,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.3,
                presence_penalty=0.3,
                stop=["You:", "Kirby:"]
            )
            if response != 0:
                for choice in response.choices:
                    last_openai_request[message.author].update(prompt, choice.text)
                    await message.channel.send('{0.text}'.format(choice))
        elif data.startswith(COMMAND_ENABLE):
            enabled_channels[hash(message.channel)] = JUMP_IN_PROBABILITY_DEFAULT
            print('Kirby enabled for channel {0.channel}'.format(message))
            await message.channel.send("Kirby started lurking in this channel.")
        elif data.startswith(COMMAND_PRESENCE):
            await message.channel.send("Yes.")
        elif data.startswith(COMMAND_CLEAN):
            last_openai_request[message.author].clear()
            await message.channel.send("Kirby just forgot all about {0.author}".format(message))
        elif data.startswith(COMMAND_DISABLE):
            if hash(message.channel) in enabled_channels:
                del enabled_channels[hash(message.channel)]
                await message.channel.send("Kirby left this channel.")
            else:
                await message.channel.send("Kirby was not even here!")
        if data.startswith(COMMAND_SHAKESPEARE):
            response = 0
            prompt = data[len(COMMAND_SHAKESPEARE):]
            prompt += "\n\n"
            response = openai.Completion.create(
                engine="davinci-instruct-beta",
                prompt=prompt,
                temperature=0.9,
                max_tokens=500,
                top_p=0.3,
                frequency_penalty=0.5,
                presence_penalty=0.2,
                stop=["\n\n\n"]
            )
            print(prompt, response)
            if response != 0:
                for choice in response.choices:
                    last_openai_request[message.author].update(prompt, choice.text)
                    await message.channel.send('{0.text}'.format(choice))
        if data.startswith(COMMAND_MARV):
            response = 0
            prompt = ""
            prompt = data[len(COMMAND_MARV):]
            openai_prompt = MARV_PROMPT.format(prompt)
            print('Prompt: {0}'.format(openai_prompt))
            response = openai.Completion.create(
                engine="curie-instruct-beta",
                prompt=openai_prompt,
                temperature=0.5,
                max_tokens=60,
                top_p=0.3,
                frequency_penalty=0.5,
                presence_penalty=0.1,
                stop=["Marv:", "You:"]
            )
            if response != 0:
                for choice in response.choices:
                    last_openai_request[message.author].update(prompt, choice.text)
                    await message.channel.send('{0.text}'.format(choice))
        else: # Random responses
            if hash(message.channel) not in enabled_channels: return 
            if enabled_channels[hash(message.channel)] <= random.randint(0, 99): return

            prompt = "This is a conversation between Kirby, god of all beings and his subjects.\n\n"
            prompt = "\n\nKirby god: I am Kirby. What can I do for you?"

            hisory = await message.channel.history(limit=10).flatten()
            #.flatten()
            for history_message in reversed(hisory):
                prompt += "\n\n" + str(history_message.author.name) + ": " + str(history_message.content)
                if history_message.author == client.user:
                    pass
            prompt += "\n\nKirby god: "
            print(prompt)

            response = openai.Completion.create(
                engine="curie-instruct-beta",
                prompt=prompt,
                temperature=0.9,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.3,
                presence_penalty=0.3,
                stop=[":", "Kirby god", "\n\n"]
            )
            if response != 0:
                for choice in response.choices:
                    last_openai_request[message.author].update(prompt, choice.text)
                    await message.channel.send('{0.text}'.format(choice))


intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.guilds = True
intents.reactions = True
client = MyClient(intents=intents)
client.run(DISCORD_BOT_TOKEN)
