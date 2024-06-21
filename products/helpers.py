import re

def remove_special_characters(input_string:str) -> str:
    cleaned_string = re.sub(r'[^a-zA-Z0-9_]', '', input_string)
    return cleaned_string