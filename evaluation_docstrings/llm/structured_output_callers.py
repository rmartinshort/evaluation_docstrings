import instructor
from openai import OpenAI
import google.generativeai as genai
from anthropic import Anthropic
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Type


class LLMStructuredOutputCaller(ABC):
    """
    Abstract base class for calling Large Language Models (LLMs) to generate structured output.
    """

    def __init__(self, api_key: str):
        """
        Initializes the LLMStructuredOutputCaller with an API key.

        Args:
            api_key (str): The API key for accessing the LLM.
        """
        self.api_key = api_key
        self.client = self.set_up_client()

    @abstractmethod
    def set_up_client(self) -> Any:
        """
        Abstract method to set up the client for the specific LLM.

        Returns:
            Any: The client object.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def token_counter(model_output: Dict[str, Any]) -> Dict[str, int]:
        """
        Abstract method to count the number of input and output tokens used by the LLM.

        Args:
            model_output (Dict[str, Any]): The output from the LLM.

        Returns:
            Dict[str, int]: A dictionary containing the number of input and output tokens.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
        raise NotImplementedError

    def invoke(
        self,
        input_string: str,
        system_template: dataclass,  # Ideally, replace Any with a specific type
        response_template: Type[Any],
        input_model_name: str,
        temperature: float = 0.0,
    ) -> Dict[str, Any]:
        """
        Invokes the LLM to generate structured output.

        Args:
            input_string (str): The input string to be processed by the LLM.
            system_template (Any): The system template to guide the LLM.
            response_template (Type[Any]): The expected data structure for the LLM's response.
            input_model_name (str): The name of the LLM to use.
            temperature (float, optional): The temperature to use for generating the output. Defaults to 0.0.

        Returns:
            Dict[str, Any]: A dictionary containing the metadata and the model dump of the LLM's response, or an empty dictionary if an error occurs.
        """
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
    def craft_input(string_input: str, system_template: Any) -> List[Dict[str, str]]:
        """
        Crafts the input messages for the LLM.

        Args:
            string_input (str): The input string from the user.
            system_template (Any): The system template to guide the LLM.

        Returns:
            List[Dict[str, str]]: A list of dictionaries representing the messages to be sent to the LLM.
        """
        messages = [
            {
                "role": "system",
                "content": system_template.system_template,
            },
            {"role": "user", "content": string_input},
        ]
        return messages


class GeminiStructuredOutputCaller(LLMStructuredOutputCaller):
    """
    A class for calling the Gemini LLM to generate structured output.
    """

    def __init__(self, api_key: str, model: str):
        """
        Initializes the GeminiStructuredOutputCaller with an API key and model name.

        Args:
            api_key (str): The API key for accessing the Gemini LLM.
            model (str): The name of the Gemini model to use.
        """
        self.api_key = api_key
        self.client = self.set_up_client(model)
        self.model_name = model

    def set_up_client(self, model: str) -> Any:
        """
        Sets up the client for the Gemini LLM.

        Args:
            model (str): The name of the Gemini model to use.

        Returns:
            Any: The Gemini client object.
        """
        genai.configure(api_key=self.api_key)
        client = instructor.from_gemini(
            client=genai.GenerativeModel(
                model_name=f"models/{model}",
            ),
            mode=instructor.Mode.GEMINI_JSON,
        )
        return client

    def invoke(
        self,
        system_template: dataclass,
        response_template: Type[Any],
        input_string: str,
        input_model_name: str = None,
        temperature: float = 0.0,
    ) -> Dict[str, Any]:
        """
        Invokes the Gemini LLM to generate structured output.

        Args:
            input_string (str): The input string to be processed by the LLM.
            system_template (Any): The system template to guide the LLM.
            response_template (Type[Any]): The expected data structure for the LLM's response.
            temperature (float, optional): The temperature to use for generating the output. Defaults to 0.0.

        Returns:
            Dict[str, Any]: A dictionary containing the metadata and the model dump of the LLM's response, or an empty dictionary if an error occurs.
        """
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
    def token_counter(model_output: Dict[str, Any]) -> Dict[str, int]:
        """
        Counts the number of input and output tokens used by the Gemini LLM.

        Args:
            model_output (Dict[str, Any]): The output from the Gemini LLM.

        Returns:
            Dict[str, int]: A dictionary containing the number of input and output tokens.
        """
        usage_stats = model_output["metadata"].usage_metadata
        input_tokens = usage_stats.prompt_token_count
        output_tokens = usage_stats.candidates_token_count
        return {"input_tokens": input_tokens, "output_tokens": output_tokens}


class OpenAIStructuredOutputCaller(LLMStructuredOutputCaller):
    """
    A class for calling the OpenAI LLM to generate structured output.
    """

    def set_up_client(self) -> Any:
        """
        Sets up the client for the OpenAI LLM.

        Returns:
            Any: The OpenAI client object.
        """
        client = instructor.from_openai(
            OpenAI(api_key=self.api_key), mode=instructor.Mode.TOOLS_STRICT
        )
        return client

    @staticmethod
    def token_counter(model_output: Dict[str, Any]) -> Dict[str, int]:
        """
        Counts the number of input and output tokens used by the OpenAI LLM.

        Args:
            model_output (Dict[str, Any]): The output from the OpenAI LLM.

        Returns:
            Dict[str, int]: A dictionary containing the number of input and output tokens.
        """
        usage_stats = model_output["metadata"].usage
        input_tokens = usage_stats.prompt_tokens
        output_tokens = usage_stats.completion_tokens
        return {"input_tokens": input_tokens, "output_tokens": output_tokens}


class AnthropicStructuredOutputCaller(LLMStructuredOutputCaller):
    """
    A class for calling the Anthropic LLM to generate structured output.
    """

    def set_up_client(self) -> Any:
        """
        Sets up the client for the Anthropic LLM.

        Returns:
            Any: The Anthropic client object.
        """
        client = instructor.from_anthropic(Anthropic(api_key=self.api_key))
        return client

    @staticmethod
    def token_counter(model_output: Dict[str, Any]) -> Dict[str, int]:
        """
        Counts the number of input and output tokens used by the Anthropic LLM.

        Args:
            model_output (Dict[str, Any]): The output from the Anthropic LLM.

        Returns:
            Dict[str, int]: A dictionary containing the number of input and output tokens.
        """
        usage_stats = model_output["metadata"].usage
        input_tokens = usage_stats.input_tokens
        output_tokens = usage_stats.output_tokens
        return {"input_tokens": input_tokens, "output_tokens": output_tokens}
