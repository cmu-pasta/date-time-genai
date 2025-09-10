import os
import sys
import time

import anthropic
import google.generativeai as genai
from openai import OpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class Model:
    def __init__(self, model_name):
        pass

    def sample(self, system_prompt, user_prompt, n):
        pass


class OpenAIModel(Model):
    def __init__(self, model_name):
        self.client = OpenAI()
        self.model_name = model_name

    def sample(self, system_prompt, user_prompt, n=1):
        samples = []
        message = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=message,
            n=n,
            # temperature=config.SAMPLING_TEMPERATURE,
        )
        samples = [r.message.content for r in response.choices]
        return samples


class GeminiModel(Model):
    def __init__(self, model_name):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        generation_config = {
            "max_output_tokens": config.MAX_TOKENS,
            "temperature": config.SAMPLING_TEMPERATURE,
            "candidate_count": 1,
        }

        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
        )
        self.model_name = model_name

    def sample(self, system_prompt, user_prompt, n=1):
        message = system_prompt + "\n" + user_prompt
        samples = []
        for i in range(n):
            response = None
            while response is None:
                try:
                    response = self.model.generate_content(message)
                    # print(f"Sampled from gemini. {i}")
                    time.sleep(10)
                except Exception as e:
                    print(f"Exception from gemini: {e}")
                    time.sleep(30)
            try:
                samples.append(response.text)
            except Exception as e:
                print(f"Exception from gemini: {e}")
                time.sleep(30)
        return samples


class AnthropicModel(Model):
    def __init__(self, model_name):
        self.client = anthropic.Anthropic()
        self.model_name = model_name

    def sample(self, system_prompt, user_prompt, n=1):
        samples = []
        message = [
            {"role": "user", "content": user_prompt},
        ]
        for i in range(n):
            response = None
            while response is None:
                try:
                    response = self.client.messages.create(
                        model=self.model_name,
                        max_tokens=config.MAX_TOKENS,
                        system=system_prompt,
                        messages=message,
                        temperature=config.SAMPLING_TEMPERATURE,
                    )
                    # print(f"Sampled from anthropic. {i}")
                except Exception as e:
                    print(f"Exception from anthropic: {e}")
                    time.sleep(10)
            samples.append(response.content[0].text)
        return samples
