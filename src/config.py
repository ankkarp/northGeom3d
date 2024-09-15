import yaml

def load_config():
    """
    Load configuration from config.yaml file.

    Returns:
        dict: Configuration.
    """
    with open("./config.yaml", "r", encoding='utf-8') as f:
        return yaml.safe_load(f)

config = load_config()