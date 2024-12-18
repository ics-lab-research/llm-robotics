import os
import io
import json
import re
import sys
import logging
import tqdm
from dataclasses import dataclass, asdict
from typing import List, Optional, Sequence

from google.api_core import retry
import google.generativeai as genai


@dataclass
class GeminiGenerationArguments:
    max_output_tokens: int = 1800
    temperature: float = 0.2
    top_p: float = 1.0
    # top_k: int = 40  # NOTE: we don't know how many
    candidate_count: int = 1
    stop_sequences: Optional[Sequence[str]] = None  # NOTE: ???
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    response_mime_type: str = "text/plain"  # additional params (json or text)


def _make_w_io_base(f, mode: str):
    if not isinstance(f, io.IOBase):
        f_dirname = os.path.dirname(f)
        if f_dirname != "":
            os.makedirs(f_dirname, exist_ok=True)
        f = open(f, mode=mode)
    return f


def _make_r_io_base(f, mode: str):
    if not isinstance(f, io.IOBase):
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


def jload(f, mode="r"):
    """Load a .json file into a dictionary."""
    f = _make_r_io_base(f, mode)
    jdict = json.load(f)
    f.close()
    return jdict


def encode_prompt(prompt_instructions):
    # NOTE: Unbound warning
    idx = 0

    """Encode multiple prompt instructions into a single string."""
    prompt = open("./prompts/prompt2.txt").read() + "\n"

    for idx, task_dict in enumerate(prompt_instructions):
        (instruction, input, output) = (
            task_dict["instruction"],
            task_dict["input"],
            task_dict["output"],
        )
        instruction = re.sub(r"\s+", " ", instruction).strip().rstrip(":")
        input = "<noinput>" if input.lower() == "" else input
        prompt += "###\n"
        prompt += f"{idx + 1}. Instruction: {instruction}\n"
        prompt += f"{idx + 1}. Input:\n{input}\n"
        prompt += f"{idx + 1}. Output:\n{output}\n"
    prompt += "###\n"

    # NOTE: Unbound warning
    prompt += f"{idx + 2}. Instruction:"
    return prompt


def seed_instruction_data_loader(seed_tasks_path: str = "./seed_tasks.json"):
    """
    NOTE: we can change format of seed tasks
    """
    # seed_tasks = [json.loads(seed) for seed in open(seed_tasks_path, "r")]
    with open(seed_tasks_path, "r", encoding="utf-8") as file:
        seed_tasks = json.load(file)  # Load JSON data directly

    seed_instruction_data = [
        {
            "instruction": t["instruction"],
            "input": t["input"],
            "output": t["output"],
        }
        for t in seed_tasks
    ]

    print(f"Loaded {len(seed_instruction_data)} human-written seed instructions")
    return seed_instruction_data


def machine_instruction_data_loader(
    generated_instruction_path="./prompts/gen_instructions.json",
) -> List:
    """
    load generated instruction if available
    """
    machine_instruction_data = []
    if os.path.exists(generated_instruction_path):
        machine_instruction_data = jload(generated_instruction_path)
        print(f"Loaded {len(machine_instruction_data)} machine-generated instructions")

        return machine_instruction_data
    else:
        return []


def gemini_completion(
    # prompts: Union[str, Sequence[str], Sequence[dict[str, str]], dict[str, str]],
    prompts: List[str],
    decoding_args: GeminiGenerationArguments,
    model_name="gemini-2.0-flash-exp",  # TODO: change to pro
    # sleep_time=2,
    batch_size=1,
    max_instances=sys.maxsize,
    max_batches=sys.maxsize,
    return_text=False,
):
    # check input is single prompt
    # is_single_prompt = isinstance(prompts, (str, dict))
    # if is_single_prompt:
    #     prompts = list(prompts)

    # if max_batches < sys.maxsize:
    #     logging.warning(
    #         "`max_batches` will be deprecated in the future, please use `max_instances` instead."
    #         "Setting `max_instances` to `max_batches * batch_size` for now."
    #     )
    #     max_instances = max_batches * batch_size

    # # NOTE: why have to define max_instances??
    # prompts = prompts[:max_instances]
    # num_prompts = len(prompts)
    # prompt_batches = [
    #     prompts[batch_id * batch_size : (batch_id + 1) * batch_size]
    #     for batch_id in range(int(math.ceil(num_prompts / batch_size)))
    # ]

    completions = []

    for _, prompt_batch in tqdm.tqdm(
        enumerate(prompts),
        desc="prompt_batches",
        total=len(prompts),
    ):
        while True:
            try:
                shared_kwargs = asdict(decoding_args)
                model = genai.GenerativeModel(
                    model_name=model_name,
                    generation_config=genai.GenerationConfig(
                        **shared_kwargs,
                    ),
                )

                completion_batch = model.generate_content(
                    prompt_batch,
                    request_options={
                        "retry": retry.Retry(
                            predicate=retry.if_transient_error,
                            initial=2.0,
                            maximum=64.0,
                            multiplier=2.0,
                            timeout=600,
                        )
                    },
                )

                # NOTE: add more information
                result = {}
                result["text"] = completion_batch.text
                result["total_tokens"] = (
                    completion_batch.usage_metadata.total_token_count
                )
                completions.append(result)

                break
            except Exception as e:
                logging.warning(f"An unexpected error occurred: {e}")

        # NOTE: we removed some code for only 1 type of response

    return completions
