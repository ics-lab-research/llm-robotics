import json
import os
import random
import re
from rouge_score import rouge_scorer
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from the .env file
load_dotenv()

seed_tasks_path = "./seed_tasks_code.jsonl"
num_instructions_to_generate = 100
request_batch_size = 5
num_prompt_instructions = 3


def encode_prompt(prompt_instructions):
    """Encode multiple prompt instructions into a single string."""
    prompt = open("./prompt.txt").read() + "\n"

    for idx, task_dict in enumerate(prompt_instructions):
        (instruction, input, output) = (
            task_dict["instruction"],
            task_dict["input"],
            task_dict["output"],
        )
        instruction = re.sub(r"\s+", " ", instruction).strip().rstrip(":")
        input = "<noinput>" if input.lower() == "" else input
        prompt += f"###\n"
        prompt += f"{idx + 1}. Instruction: {instruction}\n"
        prompt += f"{idx + 1}. Input:\n{input}\n"
        prompt += f"{idx + 1}. Output:\n{output}\n"
    prompt += f"###\n"
    prompt += f"{idx + 2}. Instruction:"
    return prompt


seed_tasks = [json.loads(l) for l in open(seed_tasks_path, "r")]
seed_instruction_data = [
    {
        "instruction": t["instruction"],
        "input": t["instances"][0]["input"],
        "output": t["instances"][0]["output"],
    }
    for t in seed_tasks
]
print(f"Loaded {len(seed_instruction_data)} human-written seed instructions")

# os.makedirs(output_dir, exist_ok=True)
request_idx = 0
# load the LM-generated instructions
machine_instruction_data = []

# load from regen.json, if empty do nothing

# if os.path.exists(os.path.join(output_dir, "regen.json")):
#     machine_instruction_data = utils.jload(os.path.join(output_dir, "regen.json"))
#     print(f"Loaded {len(machine_instruction_data)} machine-generated instructions")

# similarities = {}
# use this for tokenize instruction
scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=False)

# now let's generate new instructions!
# progress_bar = tqdm.tqdm(total=num_instructions_to_generate)
# if machine_instruction_data:
#     progress_bar.update(len(machine_instruction_data))

# first we tokenize all the seed instructions and generated machine instructions
all_instructions = [d["instruction"] for d in seed_instruction_data] + [
    d["instruction"] for d in machine_instruction_data
]

# split words in instruction
all_instruction_tokens = [scorer._tokenizer.tokenize(inst) for inst in all_instructions]

# print(all_instructions[10])
# print(all_instruction_tokens[10])

# while len(machine_instruction_data) < num_instructions_to_generate:
#     request_idx += 1

# 100 loop
# while len(machine_instruction_data) < num_instructions_to_generate:

batch_inputs = []

for _ in range(request_batch_size):  # 5
    # only sampling from the seed tasks
    prompt_instructions = random.sample(seed_instruction_data, num_prompt_instructions)
    prompt = encode_prompt(prompt_instructions)
    batch_inputs.append(prompt)

print(batch_inputs[2])

genai.configure(api_key=os.environ["GEMINI_API"])

# Create the model
# stream is false by default
generation_config = {
    "max_output_tokens": 1800,
    "temperature": 0.2,
    "top_p": 1.0,
    "candidate_count": 1,
    "top_k": 40,
    "stop_sequences": None,
    "presence_penalty": 0.0,
    "frequency_penalty": 0.0,
    "response_mime_type": "text/plain",  # additional params (json or text)
}

# @dataclasses.dataclass
# class GeminiDecodingArguments(object):
#     max_tokens: int = 1800
#     temperature: float = 0.2
#     top_p: float = 1.0
#     n: int = 1
#     stream: bool = False
#     stop: Optional[Sequence[str]] = None
#     presence_penalty: float = 0.0
#     frequency_penalty: float = 0.0
#     suffix: Optional[str] = None
#     logprobs: Optional[int] = None
#     echo: bool = False

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

chat_session = model.start_chat(history=[])

response = chat_session.send_message(batch_inputs[1])

print(response.text)
