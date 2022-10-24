"""Read config file."""
import configparser

# Method to read config file settings
def read_config(filename: str) -> configparser.ConfigParser:
    """Read specified config file.

    Args:
        filename (str): filename

    Returns:
        _type_: ConfigParser
    """
    config = configparser.ConfigParser()
    config.read(filename)
    return config
