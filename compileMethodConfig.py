import json, os, sys, re
from pathlib import Path

def extract_class_configs(folder_path_str):
    folder_path = Path(folder_path_str)
    result_dict = {}

    # Regex to find the start of a class definition
    class_regex = re.compile(r"^class\s+(\w+)")

    # Regex to find config keys inside methodConfigDict["key"] or methodConfigDict['key']
    config_regex = re.compile(r'methodConfigDict\s*\[\s*["\']([^"\']+)["\']\s*\]')

    # Iterate ONLY through the top-level folder (no recursion)
    for file_path in folder_path.glob("*.py"):
        if not file_path.is_file():
            continue

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Skipping file {file_path.name} due to read error: {e}")
            continue

        current_class = None
        in_init = False
        indent_level = 0

        # Process the file line by line to accurately track the active class and __init__ scope
        for line in content.splitlines():
            # Check for a new class definition at the start of a line
            class_match = class_regex.match(line)
            if class_match:
                current_class = class_match.group(1)
                result_dict[current_class] = []
                in_init = False
                continue

            # If we are inside a class, look for the __init__ method
            if current_class:
                # Detect the start of the __init__ function
                #if "def __init__" in line:
                if "def init" in line:
                    in_init = True
                    # Calculate indent level of __init__ to know when it ends
                    indent_level = len(line) - len(line.lstrip())
                    continue

                # If we are inside __init__, check if we left its indentation scope
                if in_init:
                    stripped = line.lstrip()
                    if stripped:  # Skip empty lines
                        current_indent = len(line) - len(stripped)
                        # If indent drops back or remains equal to __init__ definition, we left __init__
                        if current_indent <= indent_level and not stripped.startswith(
                            "def"
                        ):
                            in_init = False

                # If we are actively inside the __init__ scope, extract config names
                if in_init:
                    matches = config_regex.findall(line)
                    for match in matches:
                        if match not in result_dict[current_class]:
                            result_dict[current_class].append(match)

    # Filter out any classes that didn't end up having any configs found
    final_dict = {k: v for k, v in result_dict.items() if v}

    # Save the output to methodConfigDict.json inside the target folder
    output_file = folder_path / "methodConfigDict.json"
    try:
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(final_dict, json_file, indent=4)
        print(f"Successfully generated config map at: {output_file}")
    except Exception as e:
        print(f"Failed to write JSON file: {e}")


# --- Execution ---
if __name__ == "__main__":
    if 2==len(sys.argv):
        target_folder = sys.argv[1]
    else:
        target_folder = os.getcwd()
    extract_class_configs(target_folder)
