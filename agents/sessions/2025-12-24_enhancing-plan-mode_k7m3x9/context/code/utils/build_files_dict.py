import re

def build_files_dict(content_string):
    """
    Extract file paths and their contents from a formatted string.
    
    Args:
        content_string (str): String containing file paths and contents in the format:
                              'File: /path/to/file.py\n```py\n[content]\n```'
    
    Returns:
        dict: Dictionary mapping file paths to their contents
    """
    # Pattern to match file paths and their contents
    pattern = r'File: (.*?)\n```.*?\n(.*?)```'
    
    # Find all matches using regex with DOTALL flag to match across line breaks
    matches = re.findall(pattern, content_string, re.DOTALL)
    
    # Create a dictionary mapping file paths to their contents
    files_dict = {}
    for file_path, content in matches:
        files_dict[file_path.strip()] = content.strip()
    
    return files_dict