import re

def extract_value(pattern, line, default=None):
    """Helper to safely extract values from lines"""
    match = re.search(pattern, line)
    return match.group(1) if match else default