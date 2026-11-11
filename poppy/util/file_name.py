import os
import re


def replace_last_filename_word(file_name: str) -> str:
    name = str(file_name or "").strip()
    stem, extension = os.path.splitext(name)
    if not extension or extension == "." or not stem.strip():
        return name
    renamed_stem = re.sub(r"\S+$", "Infinity", stem)
    return f"{renamed_stem}{extension}"
