import os
import re


def replace_last_filename_word(file_name: str) -> str:
    name = str(file_name or "").strip()
    stem, extension = os.path.splitext(name)
    if not extension or extension == "." or not stem.strip():
        return name
    parts = [part for part in re.split(r"[\s._]+", stem.strip()) if part]
    if not parts:
        return name
    parts[-1] = "infinity"
    return f"{'.'.join(parts)}{extension}"
