import io
import os
import json
from typing import Dict

# import tokenize
# from nltk.translate.bleu_score import sentence_bleu


def _make_r_io_base(f, mode: str):
    if not isinstance(f, io.IOBase):
        f = open(f, mode=mode)
    return f


def jload(f, mode="r"):
    """Load a .json file into a dictionary."""
    f = _make_r_io_base(f, mode)
    jdict = json.load(f)
    f.close()
    return jdict


def test_instruction_data_loader(
    test_instruction_path="./test_instructions.json",
):
    """
    load test instruction (about 100 samples)
    """
    test_instruction_data = []
    if os.path.exists(test_instruction_path):
        test_instruction_data = jload(test_instruction_path)
        print(f"Loaded {len(test_instruction_data)} test instructions")
        return test_instruction_data
    else:
        return []


def merge_instruction_input(data_dict: Dict[str, str]) -> str:
    NO_INPUT_MARKER = "<no_input>"
    if "instruction" not in data_dict or "input" not in data_dict:
        return ""
    instruction = data_dict["instruction"]
    input_str = data_dict["input"]

    if input_str == NO_INPUT_MARKER:
        merged_prompt = f"{instruction}"
    else:
        merged_prompt = f"{instruction}[[\nYour input is:\n{input_str}]]"
    return merged_prompt


def remove_endoftext(text):
    return text.replace("<|endoftext|>", "")
