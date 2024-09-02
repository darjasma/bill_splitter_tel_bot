import re


def parse_new(input_string: str):
    # Define the regular expression pattern
    pattern = re.compile(
        r'^new\s*\n'  # Starts with "new" followed by optional spaces and a newline
        r'(?P<description>.*?)\s*\n'  # Description (possibly multiline) with optional trailing spaces and a newline
        r'(\s*(?P<sign>[+-])\s*'  # Match + or - with optional spaces around it
        r'(?P<name>[a-zA-Z]+)\s*'  # Name (chars) with optional spaces around it
        r'(?P<value>\d+)\s*)+',  # Value (numbers) with optional spaces around it, and allow multiple sequences
        re.DOTALL  # DOTALL flag to allow multi-line descriptions
    )

    # Try to match the pattern to the input string
    match = pattern.match(input_string.strip())

    if not match:
        raise ValueError("Input string does not match the expected format.")

    # Extract the description part
    description = match.group("description").strip()
    sequences = []

    # Find all sequences
    for seq in re.finditer(
            r'(?P<sign>[+-])\s*(?P<name>[a-zA-Z]+)\s*(?P<value>\d+)',
            match.group(0), re.DOTALL):
        sequences.append({
            "sign": seq.group("sign"),
            "name": seq.group("name"),
            "value": seq.group("value"),
        })

    # Return the parsed components
    return {
        "description": description,
        "sequences": sequences
    }


def parse_add_person(input_string: str):
    parts = input_string.strip().split()
    if len(parts) != 3 or parts[0] != 'add_person':
        raise ValueError("Invalid input format. Expected format: 'add_person name user_name'")
    return {
        'name': parts[1],
        'user_name': parts[2]
    }


def parse_remove_person(input_string: str):
    parts = input_string.strip().split(maxsplit=1)
    if len(parts) != 2 or parts[0] != 'remove_person':
        raise ValueError("Invalid input format. Expected format: 'remove_person name'")
    return {'name': parts[1]}

