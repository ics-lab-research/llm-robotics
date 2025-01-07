import os
import json
import requests
import fire
from tqdm import tqdm
from dotenv import load_dotenv

from utils import (
    instruction_data_loader,
    merge_instruction_input,
    remove_endoftext,
    machine_output_data_loader,
    jdump,
    extract_first_code_block,
)

# load from .env file
load_dotenv(dotenv_path="../.env")


def get_output_from_colab(instruction: str) -> str:
    # Determine the URL based on the NGROK_URL environment variable
    ngrok_url = os.environ.get("NGROK_URL")
    url = (
        ngrok_url + "/generate"
        if ngrok_url
        else "http://localhost:5000/generate"
    )

    # Create the payload dictionary
    payload = {
        "messages": [{"role": "user", "content": instruction}],
        "max_new_tokens": 10,
    }

    # Set the headers to indicate the request body is in JSON format
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()

        return response.text

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return ""


# use for-loop to get instructions
def get_output(
    output_path: str = "./results/output.json",
):
    instruction_data = instruction_data_loader()
    machine_output_data = machine_output_data_loader()
    progress_bar = tqdm(total=len(instruction_data))

    if machine_output_data:
        progress_bar.update(len(machine_output_data))

    while len(machine_output_data) < len(instruction_data):
        idx = len(machine_output_data)
        item = instruction_data[idx]
        new_instruction = merge_instruction_input(item)
        output = get_output_from_colab(new_instruction)

        machine_output_data.append(
            {
                "instruction": item["instruction"],
                "input": item["input"],
                # "output": remove_endoftext(output),
                "output": extract_first_code_block(remove_endoftext(output)),
            }
        )

        # try to save data
        jdump(machine_output_data, output_path)

        progress_bar.update(1)


def main(task, **kwargs):
    globals()[task](**kwargs)


if __name__ == "__main__":
    fire.Fire(main)
