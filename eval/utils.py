import io
import os
import json
import re
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


def instruction_data_loader(
    instruction_path="./test_instructions.json",
):
    """
    load test instruction (about 100 samples)
    """
    test_instruction_data = []
    if os.path.exists(instruction_path):
        test_instruction_data = jload(instruction_path)
        print(
            f"Loaded {len(test_instruction_data)} test instructions from {instruction_path}"
        )
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


def machine_output_data_loader(
    generated_output_path="./results/output.json",
):
    """
    load output
    """
    test_instruction_data = []
    if os.path.exists(generated_output_path):
        test_instruction_data = jload(generated_output_path)
        print(f"Loaded {len(test_instruction_data)} test instructions")
        return test_instruction_data
    else:
        return []


def _make_w_io_base(f, mode: str):
    if not isinstance(f, io.IOBase):
        f_dirname = os.path.dirname(f)
        if f_dirname != "":
            os.makedirs(f_dirname, exist_ok=True)
        f = open(f, mode=mode)
    return f


def jdump(obj, f, mode="w", indent=4, default=str):
    """Dump a str or dictionary to a file in json format.

    Args:
        obj: An object to be written.
        f: A string path to the location on disk.
        mode: Mode for opening the file.
        indent: Indent for storing json dictionaries.
        default: A function to handle non-serializable entries; defaults to `str`.
    """
    f = _make_w_io_base(f, mode)
    if isinstance(obj, (dict, list)):
        json.dump(obj, f, indent=indent, default=default)
    elif isinstance(obj, str):
        f.write(obj)
    else:
        raise ValueError(f"Unexpected type: {type(obj)}")
    f.close()


def extract_first_code_block(text):
    match = re.search(r"```(.*?)\n```", text, re.DOTALL)
    if match:
        return f"```{match.group(1)}\n```"
    return None
