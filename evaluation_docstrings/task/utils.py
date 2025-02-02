def read_code_into_dict(file_path: str) -> dict:
    """
    Reads a file and returns its contents as a dictionary with line numbers as keys and lines of code as values.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        dict: A dictionary where keys are line numbers (int) and values are the corresponding lines of code (str).
    """
    result = {}
    try:
        with open(file_path, "r") as file:
            for line_number, line in enumerate(file, start=1):
                result[line_number] = (
                    line.rstrip()
                )  # Remove trailing newline characters
    except FileNotFoundError:
        return {"Error": f"File '{file_path}' not found."}
    except Exception as e:
        return {"Error": f"An error occurred: {e}"}

    return result


def convert_code_dict_to_string(code_dict: dict, add_line_number=True) -> str:
    res = ""
    for line_number, code_line in code_dict.items():
        if add_line_number:
            res += f"{line_number} {code_line}\n"
        else:
            res += code_line + "\n"
    return res


def fix_indentation(docstring, indented_spaces):
    lines = docstring.split("\n")
    res = ""
    for line in lines:
        res += " " * indented_spaces + line + "\n"
    return res


def format_result_as_string(row):
    res = ""
    docstrings = row["docstrings"]
    if not docstrings:
        return "No docstrings"

    for element in docstrings:
        res += "-" * 20 + "\n"
        line_num = element["line_number"]
        object_name = element["object_name"]
        doc = element["docstring"]
        res += f"Line number: {line_num}\nObject name: {object_name}\n\nDocstring:\n\n{doc.strip()}\n"

    return res
