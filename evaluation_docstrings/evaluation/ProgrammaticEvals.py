class ProgrammaticEvals:
    @staticmethod
    def check_correct_fields(docstrings_dict):
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
    def check_explanation_word_count(docstrings_dict, min_words=10, max_words=50):
        if not docstrings_dict["suitable_code"]:
            return True

        for docstring in docstrings_dict["docstrings"]:
            words_in_string = docstring["docstring"].split("\n\n")[0].split()
            if (min_words > len(words_in_string)) or (len(words_in_string) > max_words):
                return False

        return True

    @staticmethod
    def check_line_numbers_and_methods(docstrings_dict, input_code):
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
