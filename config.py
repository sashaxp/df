# config.py

import json

def load_config():
    """Load configuration from a JSON file."""
    with open('config.json', 'r') as file:
        return json.load(file)

def get_config_value(key, default=None):
    """Retrieve a configuration value for a given key.

    Args:
        key (str): The configuration key.
        default: The default value to return if the key is not found.

    Returns:
        The configuration value or default if the key is not found.
    """
    config = load_config()
    return config.get(key, default)
