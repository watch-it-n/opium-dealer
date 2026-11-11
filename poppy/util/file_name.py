import os
import re

_CAPTION_FILENAME_WORD = re.compile(
    r"(?P<word>[^\W_]+)(?P<extension>\.(?:mkv|mp4)\b)",
    flags=re.IGNORECASE,
)


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


def replace_caption_filename_word(caption: str) -> str:
    parts = re.split(r"(<[^>]*>)", caption)
    return "".join(
        part
        if part.startswith("<")
        else _CAPTION_FILENAME_WORD.sub(
            lambda match: f"infinity{match.group('extension')}", part
        )
        for part in parts
    )
