import os
import json


def read_file_content(file_path):
    """Read the content of a file or return <no_input> if the file does not exist."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    return "<no_input>"


def create_samples_json(tasks_folder, output_json_file):
    """Create a JSON file with samples from subfolders."""
    samples = []

    for subfolder in os.listdir(tasks_folder):
        subfolder_path = os.path.join(tasks_folder, subfolder)
        if os.path.isdir(subfolder_path):  # Check if it's a directory
            instruction_folder = os.path.join(subfolder_path, "instruction")
            input_folder = os.path.join(subfolder_path, "input")
            output_folder = os.path.join(subfolder_path, "output")

            # Get the list of sample files (assumes same names in all subfolders)
            sample_files = (
                os.listdir(instruction_folder)
                if os.path.exists(instruction_folder)
                else []
            )

            for sample_file in sample_files:
                sample_name = os.path.splitext(sample_file)[0]

                sample = {
                    "name": sample_name,
                    "instruction": read_file_content(
                        os.path.join(instruction_folder, sample_file)
                    ),
                    "input": read_file_content(os.path.join(input_folder, sample_file)),
                    "output": read_file_content(
                        os.path.join(output_folder, sample_file)
                    ),
                }
                samples.append(sample)

    # Write the collected samples to the JSON file
    with open(output_json_file, "w", encoding="utf-8") as json_file:
        json.dump(samples, json_file, ensure_ascii=False, indent=4)


# Example usage
tasks_folder = "tasks"  # Change this to your actual folder path
output_json_file = "seed_tasks.json"
create_samples_json(tasks_folder, output_json_file)
print(f"JSON file created: {output_json_file}")
