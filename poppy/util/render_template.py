import logging
import urllib.parse

import aiohttp
import jinja2

from info import URL, LOG_CHANNEL
from poppy.bot import PoppySeedsBot
from poppy.util.human_readable import humanbytes
from poppy.util.file_properties import get_file_ids
from poppy.server.exceptions import InvalidHash

TEMPLATE_DIR = "poppy/template"


async def render_page(id: int, secure_hash: str) -> str:
    """Render an HTML page for a given file ID and hash."""
    file_data = await get_file_ids(PoppySeedsBot, int(LOG_CHANNEL), int(id))

    if file_data.unique_id[:6] != secure_hash:
        logging.debug(f"Hash mismatch for message ID {id}: expected {file_data.unique_id[:6]}, got {secure_hash}")
        raise InvalidHash

    src = urllib.parse.urljoin(
        URL,
        f"{id}/{urllib.parse.quote_plus(file_data.file_name)}?hash={secure_hash}",
    )

    media_type = file_data.mime_type.split("/")[0].strip()
    file_size = humanbytes(file_data.file_size)

    if media_type in ("video", "audio"):
        template_file = f"{TEMPLATE_DIR}/req.html"
    else:
        template_file = f"{TEMPLATE_DIR}/dl.html"
        async with aiohttp.ClientSession() as session:
            async with session.get(src) as response:
                content_length = response.headers.get("Content-Length", 0)
                file_size = humanbytes(int(content_length))

    with open(template_file) as f:
        template = jinja2.Template(f.read())

    return template.render(
        file_name=file_data.file_name.replace("_", " "),
        file_url=src,
        file_size=file_size,
        file_unique_id=file_data.unique_id,
    )