import logging
from html import escape

from pyrogram import Client, enums, filters

from database.title_requests import title_requests
from info import ADMINS

logger = logging.getLogger(__name__)


@Client.on_message(filters.private & filters.command("request"))
async def submit_title_request(client, message):
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        return await message.reply_text(
            "Send a title after the command, for example: /request Inception"
        )

    title = parts[1].strip()
    if len(title) > 200:
        return await message.reply_text("Please keep requests under 200 characters.")

    try:
        request_id = await title_requests.add(
            title,
            message.from_user.id,
        )
    except Exception:
        logger.exception("Could not save title request from user %s", message.from_user.id)
        return await message.reply_text(
            "Sorry, your request could not be saved right now. Please try again later."
        )

    await message.reply_text(
        f"Request added to the queue. Your request ID is <code>{request_id}</code>.",
        parse_mode=enums.ParseMode.HTML,
    )


@Client.on_message(filters.private & filters.command("requests") & filters.user(ADMINS))
async def list_title_requests(client, message):
    parts = (message.text or "").split(maxsplit=1)
    page_text = parts[1].strip() if len(parts) > 1 else "1"
    if not page_text.isdigit() or int(page_text) < 1:
        return await message.reply_text("Usage: /requests [page number]")

    page = int(page_text)
    try:
        requests = await title_requests.get_open(skip=(page - 1) * 5, limit=5)
    except Exception:
        logger.exception("Could not load open title requests")
        return await message.reply_text("Could not load requests right now. Please try again.")

    if not requests:
        return await message.reply_text("No open title requests on this page.")

    lines = [f"<b>Open title requests — page {page}</b>"]
    for request in requests:
        title = escape(request["title"][:80])
        if len(request["title"]) > 80:
            title += "…"
        lines.append(
            f"\n<code>{request['_id']}</code>\n{title}\n"
            f"From user <code>{request['user_id']}</code>"
        )
    lines.append("\nUse /fulfill &lt;request ID&gt; when a title is available.")
    await message.reply_text("\n".join(lines), parse_mode=enums.ParseMode.HTML)


@Client.on_message(filters.private & filters.command("myrequests"))
async def list_my_title_requests(client, message):
    try:
        requests = await title_requests.get_user_requests(message.from_user.id)
    except Exception:
        logger.exception("Could not load requests for user %s", message.from_user.id)
        return await message.reply_text("Could not load your requests right now. Please try again.")

    if not requests:
        return await message.reply_text("You haven't submitted any title requests yet.")

    lines = ["<b>Your recent title requests</b>"]
    for request in requests:
        title = escape(request["title"][:100])
        if len(request["title"]) > 100:
            title += "…"
        status = "Fulfilled" if request["status"] == "fulfilled" else "Open"
        lines.append(f"\n{title} — <b>{status}</b>")
    await message.reply_text("\n".join(lines), parse_mode=enums.ParseMode.HTML)


@Client.on_message(filters.private & filters.command("fulfill") & filters.user(ADMINS))
async def fulfill_title_request(client, message):
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        return await message.reply_text("Usage: /fulfill <request ID>")

    request_id = parts[1].strip()
    try:
        request = await title_requests.mark_fulfilled(request_id)
    except Exception:
        logger.exception("Could not fulfill title request %s", request_id)
        return await message.reply_text("Could not update that request right now. Please try again.")

    if not request:
        return await message.reply_text(
            "No open request was found with that ID. Check the ID with /requests."
        )

    try:
        await client.send_message(
            request["user_id"],
            f"Your request for <b>{escape(request['title'])}</b> has been fulfilled.",
            parse_mode=enums.ParseMode.HTML,
        )
    except Exception:
        logger.exception("Could not notify user %s about fulfilled request", request["user_id"])
        return await message.reply_text(
            "Request marked fulfilled, but I couldn't notify the user in private."
        )

    await message.reply_text(f"Marked <code>{request_id}</code> fulfilled and notified the user.")
