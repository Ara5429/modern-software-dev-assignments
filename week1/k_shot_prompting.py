import os
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 5

YOUR_SYSTEM_PROMPT = """You reverse words by listing each letter, then combining them in reverse order.

Example 1:
Input: hello
Letters: h-e-l-l-o
Reversed: o-l-l-e-h
Output: olleh

Example 2:
Input: world
Letters: w-o-r-l-d
Reversed: d-l-r-o-w
Output: dlrow

Example 3:
Input: python
Letters: p-y-t-h-o-n
Reversed: n-o-h-t-y-p
Output: nohtyp

Example 4:
Input: status
Letters: s-t-a-t-u-s
Reversed: s-u-t-a-t-s
Output: sutats

Example 5:
Input: http
Letters: h-t-t-p
Reversed: p-t-t-h
Output: ptth

Now reverse the given word using the same method. Show your work, then output ONLY the final reversed word on the last line."""

USER_PROMPT = """
Reverse the order of letters in the following word. Only output the reversed word, no other text:

httpstatus
"""

EXPECTED_OUTPUT = "sutatsptth"

def test_your_prompt(system_prompt: str) -> bool:
    for idx in range(NUM_RUNS_TIMES):
        print(f"Running test {idx + 1} of {NUM_RUNS_TIMES}")
        response = chat(
            model="mistral-nemo:12b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.5},
        )

        output_text = response['message']['content'].strip()
        print(f"Actual output: {output_text}")

        if output_text == EXPECTED_OUTPUT:
            print("SUCCESS")
            return True
        else:
            print(f"Expected: {EXPECTED_OUTPUT}")
    return False

if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)
