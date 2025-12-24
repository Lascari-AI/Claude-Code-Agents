from typing import Dict


def format_files_dict_to_xml(files_dict: Dict[str, str]) -> str:
    """Format a dictionary of files to XML format.

    Args:
        files_dict: Dictionary mapping file paths to their contents

    Returns:
        XML formatted string
    """
    output = "<files>\n"
    for file_path, content in files_dict.items():
        output += f'  <file path="{file_path}">\n'
        output += f"    <content>{content}</content>\n"
        output += f"  </file>\n"
    output += "</files>\n"
    return output
