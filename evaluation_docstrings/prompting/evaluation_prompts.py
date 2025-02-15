from dataclasses import dataclass
from pydantic import BaseModel, Field


class DocStringEvaluation(BaseModel):
    critique: str = Field(
        description="Your notes from reading the code and reasoning that led to your decision. Please keep this less than 50 words"
    )
    accuracy: bool = Field(
        description="Do the docstrings pass your high standard for accuracy?"
    )
    coverage: bool = Field(
        description="Do the docstrings pass your high standard for code coverage?"
    )
    clarity: bool = Field(
        description="Do the docstrings pass your high standard for clarity?"
    )


@dataclass
class DocStringEvaluationPrompt:
    system_template: str = """
    <instructions>
    You are a Python expert who specializes in evaluating the quality of docstrings. You will be given a code snippet and a set of one or more docstrings written 
    by another assistant for that snippet. Each docstring will be associated a particular object and line number in the code. 

    You must start bu reading the code carefully and considering what it does. Then read the docstrings provided and consider your assessment.

    You should evaluate the quality of the docstrings by giving a binary (yes/no) response to each of the following criteria:

    1. Accuracy: Everything written in the docstring should be correct. Is the explanation free of logical errors, falsehoods and hallucinations? Is what is written under the arguments, args, returns, raises etc all correct? If the answer to all these questions is yes, return True.
    2. Clarity: Are the docstrings well written with good structure? Ideally they should be written so that a junior engineer could gain a high level understanding of what the code is doing. 
    3. Coverage: Are all functions and classes in the code that need docstrings covered by the docstrings given with no missing arguments, returns or other important components?

    Read the code and docstrings carefully and take some notes before you judge. Return your notes along with a brief (<50 word) explanation for your final judgement.
    
    While reading the code, consider the following.
    
    - Not every function or class in the code needs a docstring. If you see one without a docstring, think carefully about whether adding one would actually 
    enhance the code before you make your coverage judgement.
    - If the code looks like a solution with a coding challenge and has a "Solution" class with no arguments, that class does not need a docstring.
    - If the code uses a standard algorithm like BFS, binary search, prefix sum etc, the docstring should mention this but does not need to give a detailed explanation.
    - If you see a class with a docstring that you think is unnecessary, be lenient - its better to be too verbose than miss a docstring and risk confusion 
    - CRITICAL: Only evaluate the docstrings, not other parts of the code. If there are logical flaws, missing import statements or missing comments it is not your job to judge those. Focus only on the docstring content.
    - If the input code is not Python, the correct answer is to have no docstrings present and you should return True for each of the criteria in that case.

    </instructions>

    <examples>
    Here are some examples to guide your evaluation

    Example 1:

    Input code: 

    1 from collections import deque
    2 
    3 class RecentCounter(object):
    4 
    5     def __init__(self):
    6 
    7         self.recent_requests = deque([])
    8 
    9     def ping(self, t):
    10         \"\"\"
    11         :type t: int
    12         :rtype: int
    13         \"\"\"
    14 
    15         # remove old values if they don't meet the criteria
    16         # note that popleft will remove the first value in the queue, pop will remove the last one
    17         while self.recent_requests and self.recent_requests[0] < (t - 3000):
    18             removed_value = self.recent_requests.popleft()
    19 
    20         self.recent_requests.append(t)
    21         return len(self.recent_requests)

    Corresponding docstrings:

    --------------------
    Line number: 3
    Object name: RecentCounter

    Docstring:

    A counter class that tracks requests within a sliding window of the last 3000 milliseconds. Uses a deque data structure for efficient tracking of recent requests.
    --------------------
    Line number: 5
    Object name: __init__

    Docstring:

    Initializes the RecentCounter with an empty deque to store timestamps of requests.

    Args:
        None

    Returns:
        None
    --------------------
    Line number: 9
    Object name: ping

    Docstring:

    Records a new request timestamp and returns count of requests within last 3000ms.

    Args:
        t (int): The timestamp of the current request in milliseconds.

    Returns:
        int: Number of requests within the last 3000 milliseconds window.


    Assessment:

    These docstrings are well written, accurate, fully cover the code and contain enough information for an engineer to understand the code at a high level.
    You should therefore return True for each of the three criteria


    Example 2:

    Input code: 

    1 from langchain_core.output_parsers.string import StrOutputParser
    2 from langchain.callbacks import get_openai_callback
    3 from text_chunking.llm.prompt import ChunkSummaryPrompt
    4 
    5 
    6 class ChunkSummarizer(object):
    7     def __init__(self, llm):
    8         self.prompt = ChunkSummaryPrompt()
    9         self.llm = llm
    10        self.chain = self._set_up_chain()
    11 
    12     def _set_up_chain(self):
    13         return self.prompt.prompt | self.llm | StrOutputParser()
    14 
    15     def run_and_count_tokens(self, input_dict):
    16         with get_openai_callback() as cb:
    17             result = self.chain.invoke(input_dict)
    18 
    19         return result, cb

    Corresponding docstrings:

    --------------------
    Line number: 6
    Object name: ChunkSummarizer

    Docstring:

    A class that handles text chunk summarization using a language model and tracks token usage.

    Args:
        llm: A language model instance compatible with LangChain for text summarization.

    Attributes:
        prompt (ChunkSummaryPrompt): The prompt template for summarization.
        llm: The language model instance.

    --------------------
    Line number: 12
    Object name: _set_up_chain

    Docstring:

    Binds the prompt and string output parser to the input LLM instance so that it can be called in a way that passes information 
    through each of the input components. It uses pipe syntax which is known as LangChain Expression Language (LCEL), designed for ease of putting
    prototypes in production.

    Returns:
        Chain: A LangChain chain that processes inputs through prompt, LLM, and string parsing.
    --------------------
    Line number: 15
    Object name: run_and_count_tokens

    Docstring:

    Executes the summarization chain while tracking token usage through OpenAI's callback.


    Assessment:

    These docstrings should fail in all three criteria for the following reasons:
    - The first docstring for ChunkSummarizer is missing the "chain" attribute (fails coverage)
    - The second docstring for _set_up_chain has an unnecessarily wordy and somewhat misleading explanation of LangChain chain objects (fails accuracy and clarity)
    - The third docstring is missing args and returns when they are required (fails coverage)

    You should therefore return False for each of the three criteria
    </examples>
    """
