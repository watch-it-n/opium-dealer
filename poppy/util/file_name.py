import os
import re

_CAPTION_VIDEO_EXTENSION = re.compile(
    r"\.(?P<extension>mkv|mp4)(?=(?:</[^>]+>\s*)*$)",
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


def append_infinity_to_caption_filename(caption: str) -> str:
    match = _CAPTION_VIDEO_EXTENSION.search(caption)
    if not match:
        return caption

    stem = caption[:match.start()]
    if stem.lower().endswith(".infinity"):
        return caption

    return (
        f"{stem}.Infinity.{match.group('extension')}"
        f"{caption[match.end():]}"
    )
