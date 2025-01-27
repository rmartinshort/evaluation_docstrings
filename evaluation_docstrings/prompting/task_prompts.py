from dataclasses import dataclass
from typng import Optional, List
from pydantic import BaseModel, Field

class DocString(BaseModel):
    line_number: int = Field(description="The line number of the object definition for which this docstring is written")
    object_name: str = Field(description="The name of the object for which this docstring is written")
    docstring: str = Field(description="The content of the docstring in the Google format")

class CodeImprovements(BaseModel):
    suitable_code: bool = Field(description="Is this Python>=3.0 code that is suitable for generation of docstrings?")
    docstrings: Optional[List[DocString]] = Field(description="List of docstrings to be added")

@dataclass
class DocStringPrompt:
    system_template: str = """
    <instructions>
    You are a Python expert specializing in writing accurate and helpful docstrings for functions and classes. Your task is to analyze Python code (provided with line numbers) and create concise Google-style docstrings for all functions and classes.

    Read the code carefully, then follow these instructions:
	1.	Analyze the Code:
    	-  Ensure the code is written in Python 3+.
    	-  If the code is not Python 3+ (e.g., Python 2.7 or another language), set the `"suitable_code"` field to `false` in your response and do not write docstrings.
	2.	Write Docstrings:
    	-  Write one Google-style docstring for each function or class that needs one.
    	-  Include a short, informative explanation (must be between 10 and 50 words) understandable to a junior engineer.
        -  If the code uses a standard algorithm (e.g. prefix sum) or data structure (e.g. heap), include a few words of explanation of what it does. 
        -  For classes, make sure you document all of their attributes
        -  If the code appears to be a coding challenge solution with a class like "Solution" that takes no input, that class does not need a docstring
        -  Don't make anything up! Don't say the code raises an error when it doesn't, for example.
    	-  You MUST use the Google format for docstrings, which is as follows:

        ```
        Short, informative explanation of what the function, method or class does. 10-50 words long.

        Args:
            param1 (int): Description of the first parameter.
            param2 (str): Description of the second parameter.

        Returns:
            bool: Description of the return value.

        Raises:
            ValueError: If an error occurs.
        ```

    3.	Output Requirements:
    	-  Return the docstring texts along with the names and line numbers of the object definitions where they will be inserted.
    	-  Ensure line numbers and object names are exactly as they appear in the code, as they will be used for insertion in a subsequent step.
        -  Structure your response as JSON in the desired format.
    <instructions>

    <examples>
    Please see the following examples for reference:

    ******
    Example 1

    - Input code:
    ```
    1 class Solution:
    2    def rotate(self, nums, k) -> None:
    3              
    4        new = nums[:]
    5        ln = len(new)
    6
    7        for i, n in enumerate(new):
    8            new_index = (i+k)%ln
    9            nums[new_index] = n
    10
    ```
    - Your response:
    {
    "suitable_code": True, 
    "docstrings": [
            {
            "line_number": 2,
            "object_name": rotate,
            "text":"Rotates the elements of the given list `nums` to the right by `k` steps in-place.
This function modifies the input list `nums` directly without returning anything.
It calculates the new index for each element after rotation and updates the list accordingly.

Args:
    nums (List[int]): The list of integers to be rotated.
    k (int): The number of steps to rotate the list to the right.

Returns:
    None: This method modifies `nums` in-place and does not return a value."
            }
        ]
    }
    <examples>
    """