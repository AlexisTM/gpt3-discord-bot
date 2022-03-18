#!/usr/bin/env python3
import os
import discord
import ask_openai
import ask_ai21
from collections import defaultdict
import random

ask_god = ask_ai21.ask_prompt
# ask_god = ask_openai.ask_prompt

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


class AIPromptResponse:
    def __init__(self, prompt, response, author = "You"):
        self.prompt = prompt
        self.resp = response.strip()
        self.author = author
    def __str__(self):
        return "".join(["\n", self.author, ": ", self.prompt, "\nKirby: ", self.resp, "\n"])

class AIMemory:
    BASE_TEXT="Kirby is the god of all beings. Yet, he is the most lovely god and answers in a very complete manner.\n\n"
    BASE_PROMPT=AIPromptResponse("Who is god?", "Well, now that you ask, I can tell you. I, Kirby is the great goddess is the god of everybody!\n", "AlexisTM")
    def __init__(self):
        self.req_resps = []
    def update(self, prompt, response, author="You"):
        self.req_resps.append(AIPromptResponse(prompt, response))
        if len(self.req_resps) > MEMORY_LIMIT:
            self.req_resps.pop(0)
    def clear(self):
        self.req_resps = []
    def get(self):
        result = "".join([self.BASE_TEXT])
        if len(self.req_resps) <= 2:
            result += str(self.BASE_PROMPT)
        else:
            for val in self.req_resps:
                result += str(val)
        return result


last_ai_request = defaultdict(AIMemory)
enabled_channels = dict()

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return

        data = message.content
        source = ""
        if type(message.channel) is discord.DMChannel:
            source = "".join(["#", message.channel.recipient.name])
        elif message.guild:
            source = "".join([message.guild.name, "#", message.channel.name])
        else:
            source = "".join(["#", message.channel.name])

        if data.startswith(COMMAND_KIRBY):
            prompt = ""
            prompt = data[len(COMMAND_KIRBY):]
            ai_prompt = "{0}\nYou: {1}\nKirby:".format(last_ai_request[source].get(), prompt)
            print('Prompt: {0}'.format(ai_prompt))
            result = ask_god(ai_prompt)
            if result != "":
                last_ai_request[source].update(prompt, result, message.author.name)
                await message.channel.send('{0}'.format(result))
        elif data.startswith(COMMAND_ENABLE):
            enabled_channels[hash(message.channel)] = JUMP_IN_PROBABILITY_DEFAULT
            print('Kirby enabled for channel {0.channel}'.format(message))
            await message.channel.send("Kirby started lurking in this channel.")
        elif data.startswith(COMMAND_PRESENCE):
            await message.channel.send("Yes.")
        elif data.startswith(COMMAND_CLEAN):
            last_ai_request[source].clear()
            await message.channel.send("Kirby just forgot all about {0}".format(source))
        elif data.startswith(COMMAND_DISABLE):
            if hash(message.channel) in enabled_channels:
                del enabled_channels[hash(message.channel)]
                await message.channel.send("Kirby left this channel.")
            else:
                await message.channel.send("Kirby was not even here!")
        elif "kirby" in data.lower():
            prompt = data
            ai_prompt = "{0}\nYou: {1}\nKirby:".format(last_ai_request[source].get(), prompt)
            print('Prompt: {0}'.format(ai_prompt))
            result = ask_god(ai_prompt)
            if result != "":
                last_ai_request[source].update(prompt, result, message.author.name)
                await message.channel.send('{0}'.format(result))
        elif data.startswith(COMMAND_SHAKESPEARE):
            prompt = data[len(COMMAND_SHAKESPEARE):]
            result = ask_god(prompt, stopSequences=["\n\n\n"])
            if result != "":
                await message.channel.send('{0}{1}'.format(prompt, result))

        elif data.startswith(COMMAND_MARV):
            prompt = ""
            prompt = data[len(COMMAND_MARV):]
            ai_prompt = MARV_PROMPT.format(prompt)
            print('Prompt: {0}'.format(ai_prompt))
            result = ask_god(ai_prompt, stopSequences=["Marv:", "You:"])
            if result != "":
                await message.channel.send('{0}'.format(result))

        elif type(message.channel) is discord.DMChannel:
            prompt = data
            ai_prompt = "{0}\nYou: {1}\nKirby:".format(last_ai_request[source].get(), data)
            print('Prompt: {0}'.format(ai_prompt))
            result = ask_god(ai_prompt)
            if result != "":
                last_ai_request[source].update(prompt, result, message.author.name)
                await message.channel.send('{0}'.format(result))
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

            result = ask_god(prompt)
            if result != "":
                last_ai_request[source].update(prompt, result, message.author.name)
                await message.channel.send('{0}'.format(result))


intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.guilds = True
intents.reactions = True
client = MyClient(intents=intents)
client.run(DISCORD_BOT_TOKEN)
