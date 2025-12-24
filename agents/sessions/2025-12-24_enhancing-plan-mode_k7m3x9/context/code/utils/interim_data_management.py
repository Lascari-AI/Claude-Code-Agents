import json
from pathlib import Path
from typing import Any


def save_interim_data(
    interim_data_dir: Path, data: Any, filename: str, phase_name: str
) -> str:
    """Save interim data to JSON file.

    Args:
        data: Data to save (dict, list, or Pydantic model)
        filename: Name of the file (without extension)
        phase_name: Name of the phase (e.g., 'phase1', 'phase2')

    Returns:
        Path to the saved file
    """
    phase_dir = interim_data_dir / phase_name
    phase_dir.mkdir(exist_ok=True)

    filepath = phase_dir / f"{filename}.json"

    # Handle Pydantic models
    if hasattr(data, "model_dump_json"):
        json_str = data.model_dump_json(indent=2)
        with open(filepath, "w") as f:
            f.write(json_str)
    # Handle lists of Pydantic models
    elif isinstance(data, list) and data and hasattr(data[0], "model_dump"):
        json_data = [item.model_dump() for item in data]
        with open(filepath, "w") as f:
            json.dump(json_data, f, indent=2)
    # Handle regular data
    else:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    print(f"Saved {filename} to {filepath}")
    return str(filepath)


def load_interim_data(interim_data_dir: Path, filename: str, phase_name: str) -> Any:
    """Load interim data from JSON file.

    Args:
        filename: Name of the file (without extension)
        phase_name: Name of the phase (e.g., 'phase1', 'phase2')

    Returns:
        Loaded data
    """
    filepath = interim_data_dir / phase_name / f"{filename}.json"

    if not filepath.exists():
        raise FileNotFoundError(f"Interim data file not found: {filepath}")

    with open(filepath, "r") as f:
        data = json.load(f)

    print(f"Loaded {filename} from {filepath}")
    return data
