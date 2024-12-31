import json
import re

# load content from json file
def extract_urscript_code(json_path: str):
    """Extracts URscript code from a JSON string."""
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)

    if isinstance(data, list) and data: # Check if data is a list and not empty
        output_string = data[0].get("output", "")
    else:
        return None

    # Using regex to find the code block
    match = re.search(r"```URscript\\n(.*?)\\n```", output_string, re.DOTALL)
    if match:
      return match.group(1)
    else:
       return None


# Extract and print the code
urscript_code = extract_urscript_code("./gen_instructions.json")
if urscript_code:
  print(urscript_code)
else:
    print("No URscript code block found.")
