class ProgrammaticEvals:
    @staticmethod
    def check_correct_fields(docstrings_dict: dict) -> bool:
        """
        Checks if the input dictionary has the correct fields.

        Args:
            docstrings_dict (dict): A dictionary containing docstrings information.

        Returns:
            bool: True if the dictionary has the correct fields and structure, False otherwise.
        """
        keys = set(list(docstrings_dict.keys()))
        if "summary" in keys:
            keys.remove("summary")

        if keys != {"docstrings", "suitable_code"}:
            return False

        if docstrings_dict["suitable_code"] == False:
            return True

        if not isinstance(docstrings_dict["docstrings"], list):
            return False

        if set(list(docstrings_dict["docstrings"][0].keys())) != {
            "docstring",
            "line_number",
            "object_name",
        }:
            return False

        return True

    @staticmethod
    def check_explanation_word_count(
        docstrings_dict: dict, min_words: int = 10, max_words: int = 50
    ) -> bool:
        """
        Checks if the word count of the explanation in each docstring falls within the specified range.

        Args:
            docstrings_dict (dict): A dictionary containing docstrings information.
            min_words (int, optional): The minimum number of words allowed. Defaults to 10.
            max_words (int, optional): The maximum number of words allowed. Defaults to 50.

        Returns:
            bool: True if the word count is within the range for all docstrings or if the code is not suitable, False otherwise.
        """
        if not docstrings_dict["suitable_code"]:
            return True

        for docstring in docstrings_dict["docstrings"]:
            words_in_string = docstring["docstring"].split("\n\n")[0].split()
            if (min_words > len(words_in_string)) or (len(words_in_string) > max_words):
                return False

        return True

    @staticmethod
    def check_line_numbers_and_methods(docstrings_dict: dict, input_code: str) -> bool:
        """
        Checks if the line numbers and object names in the docstrings match the input code.

        Args:
            docstrings_dict (dict): A dictionary containing docstrings information.
            input_code (str): The input code as a string.

        Returns:
            bool: True if the line numbers and object names match for all docstrings or if the code is not suitable, False otherwise.
        """
        if not docstrings_dict["suitable_code"]:
            return True

        input_code_lines = input_code[input_code.index("1") - 1 :].split("\n")
        for docstring in docstrings_dict["docstrings"]:
            object_line = docstring["line_number"]
            object_name = docstring["object_name"]
            chosen_line = input_code_lines[object_line - 1]
            if (str(object_line) not in chosen_line) or (
                object_name not in chosen_line
            ):
                return False

        return True
