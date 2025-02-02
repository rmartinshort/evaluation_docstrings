import instructor
from openai import OpenAI
import google.generativeai as genai
from anthropic import Anthropic
from abc import ABC, abstractmethod


class LLMStructuredOutputCaller(ABC):
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = self.set_up_client()

    @abstractmethod
    def set_up_client(self):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def token_counter(self):
        raise NotImplementedError

    def invoke(
        self,
        input_string,
        system_template,
        response_template,
        input_model_name,
        temperature=0,
    ):
        inputs = self.craft_input(input_string, system_template)
        try:
            res, completions = self.client.chat.completions.create_with_completion(
                model=input_model_name,
                response_model=response_template,
                temperature=temperature,
                messages=inputs,
                max_tokens=2048,
            )
        except Exception as e:
            print(f"Error calling {input_model_name}: {e}")
            return {}

        return {"metadata": completions, "model_dump": res.model_dump()}

    @staticmethod
    def craft_input(string_input, system_template):
        messages = [
            {
                "role": "system",
                "content": system_template.system_template,
            },
            {"role": "user", "content": string_input},
        ]
        return messages


class GeminiStructuredOutputCaller(LLMStructuredOutputCaller):
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.client = self.set_up_client(model)
        self.model_name = model

    def set_up_client(self, model):
        genai.configure(api_key=self.api_key)
        client = instructor.from_gemini(
            client=genai.GenerativeModel(
                model_name=f"models/{model}",
            ),
            mode=instructor.Mode.GEMINI_JSON,
        )
        return client

    def invoke(self, input_string, system_template, response_template, temperature=0):
        inputs = self.craft_input(input_string, system_template)
        try:
            res, completions = self.client.messages.create_with_completion(
                response_model=response_template,
                messages=inputs,
                generation_config={"temperature": temperature},
            )
        except Exception as e:
            print(f"Error calling {self.model_name}: {e}")
            return {}

        return {"metadata": completions, "model_dump": res.model_dump()}

    @staticmethod
    def token_counter(model_output):
        usage_stats = model_output["metadata"].usage_metadata
        input_tokens = usage_stats.prompt_token_count
        output_tokens = usage_stats.candidates_token_count
        return {"input_tokens": input_tokens, "output_tokens": output_tokens}


class OpenAIStructuredOutputCaller(LLMStructuredOutputCaller):
    def set_up_client(self):
        client = instructor.from_openai(
            OpenAI(api_key=self.api_key), mode=instructor.Mode.TOOLS_STRICT
        )
        return client

    @staticmethod
    def token_counter(model_output):
        usage_stats = model_output["metadata"].usage
        input_tokens = usage_stats.prompt_tokens
        output_tokens = usage_stats.completion_tokens
        return {"input_tokens": input_tokens, "output_tokens": output_tokens}


class AnthropicStructuredOutputCaller(LLMStructuredOutputCaller):
    def set_up_client(self):
        client = instructor.from_anthropic(Anthropic(api_key=self.api_key))
        return client

    @staticmethod
    def token_counter(model_output):
        usage_stats = model_output["metadata"].usage
        input_tokens = usage_stats.input_tokens
        output_tokens = usage_stats.output_tokens
        return {"input_tokens": input_tokens, "output_tokens": output_tokens}
