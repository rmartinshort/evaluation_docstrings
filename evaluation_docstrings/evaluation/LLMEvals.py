from evaluation_docstrings.prompting.evaluation_prompts import (
    DocStringEvaluationPrompt,
    DocStringEvaluation,
)
from typing import Any


class LLMEvals:
    """
    A class to evaluate and format results related to code and its associated docstrings.

    Methods:
        format_result_for_evaluation(input_code: str, docstrings_dict: dict) -> str:
            Formats the input code and its associated docstrings for evaluation.

        docstring_quality(llm: Any, input_code: str, docstring_to_assess: dict, model_name: str = None) -> tuple:
            Evaluates the quality of a docstring using a language model.
    """

    @staticmethod
    def format_result_for_evaluation(input_code: str, docstrings_dict: dict) -> str:
        """
        Formats the input code and its associated docstrings for evaluation.

        Args:
            input_code (str): The code to be evaluated.
            docstrings_dict (dict): A dictionary containing information about the docstrings.

        Returns:
            str: A formatted string containing the input code and evaluation results.
        """
        res = ""
        res += (
            f"<input code>:\n\n{input_code}\n<input code>\n<docstring_to_evaluate>\n\n"
        )
        if docstrings_dict["suitable_code"] is False:
            res += (
                "This code is not suitable for analysis, so no docstring was returned"
            )
            res += "\n<docstring_to_evaluate>"
            return res

        for element in docstrings_dict["docstrings"]:
            res += "-" * 20 + "\n"
            line_num = element["line_number"]
            object_name = element["object_name"]
            doc = element["docstring"]
            res += f"Line number: {line_num}\nObject name: {object_name}\n\nDocstring:\n\n{doc.strip()}\n"

        res += "\n<docstring_to_evaluate>"
        return res

    @staticmethod
    def docstring_quality(
        llm: Any, input_code: str, docstring_to_assess: dict, model_name: str = None
    ) -> tuple:
        """
        Evaluates the quality of a docstring using a language model.

        Args:
            llm (Any): The language model instance used for evaluation.
            input_code (str): The code associated with the docstring to assess.
            docstring_to_assess (dict): A dictionary containing the docstring information.
            model_name (str, optional): The name of the model to use for evaluation. Defaults to None.

        Returns:
            tuple: A tuple containing the evaluation response and the token count.
        """
        docstring_prompt = LLMEvals.format_result_for_evaluation(
            input_code, docstring_to_assess
        )
        if model_name:
            evaluation_response = llm.invoke(
                docstring_prompt,
                DocStringEvaluationPrompt,
                DocStringEvaluation,
                input_model_name=model_name,
                temperature=0,
            )
        else:
            evaluation_response = llm.invoke(
                docstring_prompt,
                DocStringEvaluationPrompt,
                DocStringEvaluation,
                temperature=0,
            )

        tokens = llm.token_counter(evaluation_response)
        return evaluation_response, tokens
