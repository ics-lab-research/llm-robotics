import os
import json
import requests
import fire
from tqdm import tqdm
from dotenv import load_dotenv

from utils import (
    test_instruction_data_loader,
    merge_instruction_input,
    remove_endoftext,
)

# load from .env file
load_dotenv(dotenv_path="../.env")


# create hello function
def hello(name):
    print(f"Hello, {name}!")


# task 1: get output of "who are you first"
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
        return None


# task 2: save output to json
# use for-loop to get instructions
def get_output(output_path: str = "./results/output.json"):
    data = test_instruction_data_loader()

    # to prevent error, we count generated output

    # dump to json file, this json file include instruction, input and output
    with open(output_path, "w") as f:
        # output_data = []
        for item in tqdm(data, desc="Getting output"):
            new_instruction = merge_instruction_input(item)
            output = get_output_from_colab(new_instruction)

            output_data.append(
                {
                    "instruction": item["instruction"],
                    "input": item["input"],
                    "output": remove_endoftext(output),
                }
            )
        json.dump(output_data, f, indent=4)


def main(task, **kwargs):
    globals()[task](**kwargs)


if __name__ == "__main__":
    fire.Fire(main)
