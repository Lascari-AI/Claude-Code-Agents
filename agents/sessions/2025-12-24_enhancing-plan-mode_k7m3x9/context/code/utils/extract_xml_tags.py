import re


def extract_xml_content(filename, tags=None):
    """
    Extract content between XML-like tags from a text file.

    Args:
        filename (str): Path to the text file
        tags (list, optional): List of tag names to extract. If None, extracts all found tags.

    Returns:
        dict: Dictionary with tag names as keys and their content as values
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()

        # Find all XML-like tags and their content
        pattern = r"<([^>]+)>([\s\S]*?)</\1>"
        matches = re.findall(pattern, content)

        # Filter by requested tags if specified
        result = {}
        for tag_name, tag_content in matches:
            if tags is None or tag_name in tags:
                result[tag_name] = tag_content.strip()

        return result

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return {}
    except Exception as e:
        print(f"Error extracting content: {str(e)}")
        return {}
