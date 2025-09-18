def sanitize_model_name_for_path(model_name: str) -> str:
    """
    Sanitize model name for safe use in file paths.

    Replaces characters that are problematic in file paths:
    - Forward slashes (/) with hyphens (-)
    - Backslashes (\) with hyphens (-)
    - Colons (:) with hyphens (-)
    - Asterisks (*) with hyphens (-)
    - Question marks (?) with hyphens (-)
    - Double quotes (") with hyphens (-)
    - Less than (<) with hyphens (-)
    - Greater than (>) with hyphens (-)
    - Pipes (|) with hyphens (-)
    - Dots (.) with hyphens (-)
    - Other potentially problematic characters

    Args:
        model_name: The original model name (e.g., "gemini/gemini-2.5-flash")

    Returns:
        Sanitized model name safe for file paths (e.g., "gemini-gemini-2.5-flash")
    """

    # Replace potentially problematic characters
    sanitized = model_name
    sanitized = sanitized.replace("\\", "-")  # Backslashes
    sanitized = sanitized.replace("/", "-")  # Forward slashes
    sanitized = sanitized.replace(":", "-")  # Colons
    sanitized = sanitized.replace("*", "-")  # Asterisks
    sanitized = sanitized.replace("?", "-")  # Question marks
    sanitized = sanitized.replace('"', "-")  # Double quotes
    sanitized = sanitized.replace("<", "-")  # Less than
    sanitized = sanitized.replace(">", "-")  # Greater than
    sanitized = sanitized.replace("|", "-")  # Pipes
    sanitized = sanitized.replace(".", "-")  # Dots

    # Remove any double hyphens that might result from replacements
    while "--" in sanitized:
        sanitized = sanitized.replace("--", "-")

    # Remove leading/trailing hyphens
    sanitized = sanitized.strip("-")

    return sanitized


# Naive prompt template
NAIVE_PROMPT_TEMPLATE = """
Your task is: {task}
"""

# Few-shot prompt template
FEW_SHOT_PROMPT_TEMPLATE = """
Here are a few examples for {language}:

{examples}

Your task:
{task}
"""
