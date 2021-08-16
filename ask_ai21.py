import requests
import os

API_URL = os.getenv("API_URL", "https://api.ai21.com/studio/v1/{}/complete")
# Set the ENV var with your AI21 Studio API key:
API_KEY = os.getenv("AI21_API_KEY")
# options are j1-jumbo and j1-large
MODEL = "j1-jumbo"

def ask_prompt(prompt, model=MODEL, num_results=1, max_tokens=250, stopSequences=["You:", "Kirby:"],
                  temperature=0.8, topP=1.0, topKReturn=2):
    """
    Helper function to send request to AI21 Studio
    :return: the JSON response from the API
    """
    res = requests.post(API_URL.format(model),
                        headers={"Authorization": f"Bearer {API_KEY}"},
                        json={
                            "prompt": prompt,
                            "numResults": num_results,
                            "maxTokens": max_tokens,
                            "stopSequences": stopSequences,
                            "temperature": temperature,
                            "topP": topP,
                            "topKReturn": topKReturn
                        })
    assert res.status_code == 200, res.json()
    
    return res.json()['completions'][0]['data']['text']

