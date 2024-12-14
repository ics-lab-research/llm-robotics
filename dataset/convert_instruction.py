import os
import glob
import json

# Folder containing the files
folder_path = "./basic"  # Replace with the folder containing your files
output_json = "dataset.json"


def create_llm_dataset(folder, output_path):
    # Find all files with -in and -out extensions
    in_files = sorted(glob.glob(os.path.join(folder, "*-in")))
    out_files = sorted(glob.glob(os.path.join(folder, "*-out")))

    # Create a dataset list
    dataset = []

    # Match files based on their prefix
    for in_file in in_files:
        prefix = os.path.basename(in_file).rsplit("-in", 1)[0]
        matching_out_file = next(
            (out for out in out_files if prefix in os.path.basename(out)), None
        )

        if matching_out_file:
            # Read instruction content and split by double newlines
            with open(in_file, "r") as infile:
                instructions = infile.read().strip().split("\n\n")

            # Read output content
            with open(matching_out_file, "r") as outfile:
                output_content = outfile.read().strip()

            # Append each instruction as a separate sample
            for instruction in instructions:
                dataset.append(
                    {
                        "instruction": instruction.strip(),
                        "input": "",  # Leave blank or customize as needed
                        "output": output_content,
                    }
                )

    # Save the dataset to JSON
    with open(output_path, "w") as jsonfile:
        json.dump(dataset, jsonfile, indent=4)


# Run the function
create_llm_dataset(folder_path, output_json)

print(f"Dataset saved to {output_json}")
