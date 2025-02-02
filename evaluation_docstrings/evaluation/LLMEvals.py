from evaluation_docstrings.prompting.evaluation_prompts import (
    DocStringEvaluationPrompt,
    DocStringEvaluation,
)


class LLMEvals:
    @staticmethod
    def format_result_for_evaluation(input_code, docstrings_dict):
        res = ""
        res += (
            f"<input code>:\n\n{input_code}\n<input code>\n<docstring_to_evaluate>\n\n"
        )
        if docstrings_dict["suitable_code"] == False:
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
    def docstring_quality(llm, input_code, docstring_to_assess, model_name=None):
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
