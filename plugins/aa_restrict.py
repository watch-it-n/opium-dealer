# Don't Remove Credit @letswatchitnow
# Subscribe YouTube Channel For Amazing Bot @letswatchitnow
# Ask Doubt on telegram @letswatchitnow

import asyncio
import re

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from info import ADMINS, GRP_LNK

_allowed_group_id = None
_allowed_group_resolved = False
_resolving_lock = None


def _parse_group_link():
    group = (GRP_LNK or "").strip()
    if not group:
        return None

    group = re.sub(r"^https?://", "", group, flags=re.IGNORECASE)
    group = re.sub(r"^telegram\.me/", "", group, flags=re.IGNORECASE)
    group = re.sub(r"^t\.me/", "", group, flags=re.IGNORECASE)
    group = group.rstrip("/")

    if group.startswith("@"):
        group = group[1:]

    if group.isdigit() or group.startswith("-100"):
        return int(group)

    return group


async def _get_allowed_group_id(client):
    global _allowed_group_id, _allowed_group_resolved, _resolving_lock

    if _resolving_lock is None:
        _resolving_lock = asyncio.Lock()

    if _allowed_group_resolved:
        return _allowed_group_id

    async with _resolving_lock:
        if _allowed_group_resolved:
            return _allowed_group_id

        target = _parse_group_link()
        print(f"[BLOCK] Resolving group target: {target}")

        if target is None:
            print("[BLOCK] GRP_LNK is empty or invalid")
            _allowed_group_resolved = True
            return None

        try:
            chat = await client.get_chat(target)
            _allowed_group_id = chat.id
            print(f"[BLOCK] Resolved group ID: {_allowed_group_id}")
        except Exception as e:
            print(f"[BLOCK] get_chat failed: {e}")
            _allowed_group_id = None

        _allowed_group_resolved = True
        return _allowed_group_id


# group=-1 means this runs BEFORE all other handlers (lower number = higher priority)
@Client.on_message(filters.private & ~filters.user(ADMINS) & filters.incoming, group=-1)
async def private_block_non_admins(_, message):
    text = (message.text or "").strip()
    if (
        (message.command and message.command[0].split("@", 1)[0].lower() == "start")
        or re.match(r"^/start(?:@\w+)?(?:\s|$)", text, flags=re.IGNORECASE)
    ):
        return

    # Normal PM search text is blocked below; /start is allowed so welcome and
    # file deep links from group results can be handled by the main start flow.
    keyboard = (
        InlineKeyboardMarkup(
            [[InlineKeyboardButton("Join Official Group", url=GRP_LNK)]]
        )
        if GRP_LNK
        else None
    )
    await message.reply_text(
        "**ACCESS DENIED.**\n"
        "Please join our official group to access the bot's features.",
        reply_markup=keyboard,
    )
    message.stop_propagation()


# group=-1 means this runs BEFORE all other handlers
@Client.on_message(filters.group & filters.incoming, group=-1)
async def group_block_unauthorized(client, message):
    if message.from_user and message.from_user.id in ADMINS:
        return

    allowed_id = await _get_allowed_group_id(client)
    print(f"[BLOCK] Chat ID: {message.chat.id} | Allowed ID: {allowed_id}")

    if allowed_id is None:
        return  # GRP_LNK misconfigured, silently allow

    if message.chat.id != allowed_id:
        await message.reply_text(
            "**ACCESS DENIED.**\n"
            "Please join our official group to access the bot's features.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Go to Official Group", url=GRP_LNK)]]
            )
            if GRP_LNK
            else None,
        )
        message.stop_propagation()
    # allowed group → do nothing, fall through to other handlers normally
