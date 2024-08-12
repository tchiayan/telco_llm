from box import ConfigBox 
import yaml 
from pathlib import Path
import os 

def read_config(file_path: Path = Path("./config.yaml")) -> ConfigBox:
    """
    Reads a configuration file and returns a ConfigBox object.

    Args:
        file_path (Path): The path to the configuration file. Defaults to "./config.yaml".

    Returns:
        ConfigBox: A ConfigBox object containing the configuration data.

    Raises:
        FileNotFoundError: If the specified configuration file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Config file with path [{file_path}] not found")

    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
        return ConfigBox(config)