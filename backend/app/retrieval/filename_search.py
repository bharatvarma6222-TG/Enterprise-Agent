import re


def extract_filename(query: str):

    match = re.search(
        r'([\w\-]+\.pdf)',
        query,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return None
