"""
batch_selfinstruct_generate.py

run:
python -m generate_instruction_gemini generate_instruction_following_data \
  --output_dir ./ \
  --num_instructions_to_generate 10 \
  --model_name="text-davinci-003" \
  --attempts=0,  # change name of output, testing purpose
"""

import fire
import os
import tqdm
import random
import time

import numpy as np
from dotenv import load_dotenv
import google.generativeai as genai
from rouge_score import rouge_scorer
from functools import partial
from multiprocessing import Pool

from utils_gemini import (
    seed_instruction_data_loader,
    machine_instruction_data_loader,
    encode_prompt,
    GeminiGenerationArguments,
    gemini_completion,
    jdump,
)

from post_process_utils import post_process_gemini_response


# Load environment variables from the .env file
load_dotenv(dotenv_path="../.env")

genai.configure(api_key=os.environ["GEMINI_API"])


def generate_instruction_following_data(
    seed_tasks_path="./prompts/seed_tasks.json",
    # generated_instruction_path="./results/gen_instructions.json",
    generated_instruction_path="./results/test_instructions.json",
    # filtered_instruction_path="./prompts/gen_instructions.json",
    num_instructions_to_generate=100,  # 20K samples
    model_name="gemini-2.0-flash-exp",  # TODO: change to pro
    num_prompt_instructions=3,
    request_batch_size=5,
    temperature=1.0,
    top_p=1.0,
    num_cpus=16,
    # attempts=0,  # change name of output, testing purpose
):
    # change name of output
    # if attempts != 0:
    #     generated_instruction_path = "./results/gen_instructions.json"

    # init some variable
    request_idx = 0
    seed_instruction_data = seed_instruction_data_loader(seed_tasks_path)
    machine_instruction_data = machine_instruction_data_loader()

    # use rouge-L for evaluate instruction
    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=False)

    # now let's generate new instructions!
    progress_bar = tqdm.tqdm(total=num_instructions_to_generate)
    if machine_instruction_data:
        progress_bar.update(len(machine_instruction_data))

    # first we tokenize all the seed instructions and generated machine instructions
    all_instructions = [d["instruction"] for d in seed_instruction_data] + [
        d["instruction"] for d in machine_instruction_data
    ]
    all_instruction_tokens = [
        scorer._tokenizer.tokenize(inst) for inst in all_instructions
    ]

    while len(machine_instruction_data) < num_instructions_to_generate:
        request_idx += 1

        batch_inputs = []
        for _ in range(request_batch_size):
            # only sampling from the seed tasks
            prompt_instructions = random.sample(
                seed_instruction_data, num_prompt_instructions
            )
            prompt = encode_prompt(prompt_instructions)
            batch_inputs.append(prompt)

        decoding_args = GeminiGenerationArguments(
            temperature=temperature,
            candidate_count=1,
            max_output_tokens=3072,
            top_p=top_p,
            stop_sequences=["\n20", "20.", "20."],
        )

        request_start = time.time()
        print(f"Calling {model_name}...")
        results = gemini_completion(
            prompts=batch_inputs,
            model_name=model_name,
            batch_size=request_batch_size,
            decoding_args=decoding_args,
        )  # list of response (string)

        request_duration = time.time() - request_start
        print(f"request took - {request_duration}")

        # try to filter responses
        process_start = time.time()
        instruction_data = []
        for result in results:
            new_instructions = post_process_gemini_response(
                num_prompt_instructions, result
            )
            instruction_data += new_instructions

        total = len(instruction_data)
        keep = 0

        # TODO: try to filter samples when code not good
        # for instruction_data_entry in instruction_data:
        #     output = instruction_data_entry["output"]

        # NOTE: try to caculate rouge score
        for instruction_data_entry in instruction_data:
            # computing similarity with the pre-tokenzied instructions
            new_instruction_tokens = scorer._tokenizer.tokenize(
                instruction_data_entry["instruction"]
            )

            with Pool(num_cpus) as p:
                rouge_scores = p.map(
                    partial(rouge_scorer._score_lcs, new_instruction_tokens),
                    all_instruction_tokens,
                )

            rouge_scores = [score.fmeasure for score in rouge_scores]
            most_similar_instructions = {
                all_instructions[i]: rouge_scores[i]
                for i in np.argsort(rouge_scores)[-10:][::-1]
            }

            if max(rouge_scores) > 0.7:
                continue
            else:
                keep += 1

            instruction_data_entry["most_similar_instructions"] = (
                most_similar_instructions
            )
            instruction_data_entry["avg_similarity_score"] = float(
                np.mean(rouge_scores)
            )
            machine_instruction_data.append(instruction_data_entry)
            all_instructions.append(instruction_data_entry["instruction"])
            all_instruction_tokens.append(new_instruction_tokens)
            progress_bar.update(1)

        process_duration = time.time() - process_start
        print(
            f"Request {request_idx} took {request_duration:.2f}s, processing took {process_duration:.2f}s"
        )
        print(f"Generated {total} instructions, kept {keep} instructions")

        jdump(machine_instruction_data, generated_instruction_path)

        # # NOTE: remember remove it before testing
        # break


def main(task, **kwargs):
    globals()[task](**kwargs)


if __name__ == "__main__":
    fire.Fire(main)
