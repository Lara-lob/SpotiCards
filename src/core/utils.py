# src/core/utils.py
import re



def sanitize_name(name: str) -> str:
    """
    Sanitize a string to be safe for use as a path.
    Args:
        name (str): Original name string
    Returns:
        str: Sanitized name string
    """
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', name)
    return sanitized.strip()[:100]