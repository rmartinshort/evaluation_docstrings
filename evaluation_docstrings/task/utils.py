from collections import defaultdict
from sklearn.metrics import cohen_kappa_score


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


def assemble_raw_match_scores(df, id_col, type_col, scores_columns):
    if not isinstance(type_col, type(None)):
        plot_df = df[[id_col, type_col]]
    else:
        plot_df = df[[id_col]]

    for k, v in scores_columns.items():
        plot_df[k] = (df[v] == df[k]).copy()

    plot_df["total_score"] = df.apply(
        lambda row: all(
            row[score_col] == row[gt_col]
            for score_col, gt_col in scores_columns.items()
        ),
        axis=1,
    )

    return plot_df


def assemble_cohen_kappa(df, scores_columns):
    result = defaultdict(str)
    for k, v in scores_columns.items():
        result[k] = cohen_kappa_score(df[k], df[v])

    return result


def format_result_for_evaluation(row):
    res = ""
    input_code = row["input_code"]
    model_output = eval(row["docstrings_list"])
    docstrings = model_output["docstrings"]
    res += f"Input code:\n\n{input_code}\n\nCorresponding docstrings:\n\n"
    for element in docstrings:
        res += "-" * 20 + "\n"
        line_num = element["line_number"]
        object_name = element["object_name"]
        doc = element["docstring"]
        res += f"Line number: {line_num}\nObject name: {object_name}\n\nDocstring:\n\n{doc.strip()}\n"

    return res
