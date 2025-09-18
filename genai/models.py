import os
import sys
import time
from enum import Enum
from typing import List

import litellm

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class ModelType(Enum):
    """Enum defining the allowed model types."""

    OPENAI = "gpt-5"
    GEMINI = "gemini/gemini-2.5-flash"
    CLAUDE = "claude-sonnet-4-20250514"


class Model:
    """Base model class providing a unified interface for all LLM providers."""

    def __init__(self, model_type: ModelType):
        """
        Initialize the model with a specific ModelType enum.

        Args:
            model_type: ModelType enum value specifying which model to use
        """
        if not isinstance(model_type, ModelType):
            raise TypeError(f"Invalid model type: {model_type}")

        self.model_type = model_type
        self.model_name = model_type.value

        # Set to True for debugging
        litellm.set_verbose = False

    def sample(self, system_prompt: str, user_prompt: str, n: int = 1) -> List[str]:
        """
        Generate samples using the specified model.

        Args:
            system_prompt: System message to set context
            user_prompt: User message/prompt
            n: Number of samples to generate

        Returns:
            List of generated text samples
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        samples = []
        for i in range(n):
            try:
                params = {
                    "model": self.model_name,
                    "messages": messages,
                    "max_tokens": config.MAX_TOKENS,
                    "temperature": config.SAMPLING_TEMPERATURE,
                    "reasoning_effort": "low",
                }

                response = litellm.completion(**params)
                content = response.choices[0].message.content
                samples.append(content)

            except Exception as e:
                print(f"Exception from {self.model_name}: {e}")
                samples.append("")

        return samples
