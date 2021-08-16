import os
import openai
openai.api_key = os.environ.get("OPENAI_KEY")

MODEL="davinci-instruct-beta"

def ask_prompt(prompt, model=MODEL, num_results=1, max_tokens=25, stopSequences=["You:", "Kirby:"],
                  temperature=0.8, topP=1.0, topKReturn=2):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=topP,
        frequency_penalty=0.3,
        presence_penalty=0.3,
        stop=stopSequences
    )
    if response != 0:
        for choice in response.choices:
            return choice.text
    return "[idk]"
